from django.db import transaction, IntegrityError
from django.db.models import OuterRef, Exists
from django.core.exceptions import ValidationError
from ..models import Journal, JournalLine
from ..exceptions.journal_exceptions import JournalAlreadyExistsError
from uuid6 import uuid7


class JournalWithLinesService:

    @staticmethod
    @transaction.atomic
    def create(data):
        journal_id = data["id"]

        # すでに同じUUIDが存在する場合
        if Journal.objects.filter(id=journal_id).exists():
            raise JournalAlreadyExistsError(journal_id)

        try:
            with transaction.atomic():
                # 仕訳ヘッダーの作成
                journal = Journal.objects.create(
                    id=journal_id,
                    recorded_date=data["recorded_date"],
                    description=data.get("description", ""),
                    type="NORMAL",
                )

                # 仕訳明細の作成
                lines_to_create = []
                for line in data["lines"]:
                    # 符号付き整数へ変換（DEBITは正、CREDITは負）
                    amount = (
                        line["amount"] if line["side"] == "DEBIT" else -line["amount"]
                    )

                    lines_to_create.append(
                        JournalLine(
                            journal=journal,
                            account_id=line["account_id"],
                            amount=amount,
                        )
                    )

                JournalLine.objects.bulk_create(lines_to_create)

        except IntegrityError:
            # すでに同じUUIDが存在する場合の再チェック
            if Journal.objects.filter(id=journal_id).exists():
                raise JournalAlreadyExistsError(journal_id)

            raise

        return journal

    @staticmethod
    @transaction.atomic
    def revise(original_journal_id: str, new_journal_data: dict) -> Journal:
        """逆仕訳、訂正仕訳の作成"""
        try:
            with transaction.atomic():
                # 元の仕訳を取得
                original_journal = (
                    Journal.objects.select_for_update()
                    .prefetch_related("lines")
                    .get(id=original_journal_id)
                )

                # 逆仕訳の自動生成
                cancel_journal_id = uuid7()
                cancel_journal = Journal.objects.create(
                    id=cancel_journal_id,
                    recorded_date=original_journal.recorded_date,
                    description=f"【取消】 {original_journal.description}",
                    type="CANCEL",
                    original_journal=original_journal,
                )

                # 逆仕訳の明細自動生成（金額を反転）
                cancel_lines = []
                for line in original_journal.lines.all():
                    cancel_lines.append(
                        JournalLine(
                            journal=cancel_journal,
                            account_id=line.account_id,
                            amount=-line.amount,
                        )
                    )
                JournalLine.objects.bulk_create(cancel_lines)

                # 訂正仕訳の作成
                new_journal_id = new_journal_data["id"]
                new_journal = Journal.objects.create(
                    id=new_journal_id,
                    recorded_date=new_journal_data["recorded_date"],
                    description=new_journal_data.get("description", ""),
                    type="NORMAL",
                    original_journal=cancel_journal,
                )

                # 訂正仕訳の明細作成
                new_lines = []
                for line in new_journal_data["lines"]:
                    amount = (
                        line["amount"] if line["side"] == "DEBIT" else -line["amount"]
                    )
                    new_lines.append(
                        JournalLine(
                            journal=new_journal,
                            account_id=line["account_id"],
                            amount=amount,
                        )
                    )
                JournalLine.objects.bulk_create(new_lines)

                return new_journal

        except Journal.DoesNotExist:
            raise ValidationError("対象の仕訳が存在しません。")
        except IntegrityError as e:
            # OneToOne制約違反が起きた場合
            raise ValidationError("この仕訳は既に修正・取消されています。")

    @staticmethod
    def list():
        """最新の正常仕訳のみを取得する"""
        has_child = Journal.objects.filter(original_journal_id=OuterRef("id"))

        journals = (
            Journal.objects.filter(type="NORMAL")
            .filter(~Exists(has_child))
            .prefetch_related("lines")
            .order_by("-recorded_date", "-id")
        )

        return journals

    @staticmethod
    def history(current_journal_id):
        """指定された仕訳の元仕訳を辿って履歴を全件取得する。"""
        ids = []
        current_id = current_journal_id

        # 対象IDを取得
        while current_id:
            ids.append(current_id)
            try:
                current_id = (
                    Journal.objects.only("original_journal_id")
                    .get(id=current_id)
                    .original_journal_id
                )
            except Journal.DoesNotExist:
                break

        # 仕訳を一括取得
        journals = Journal.objects.filter(id__in=ids).prefetch_related("lines")

        # 古い順に並び替え
        journal_map = {j.id: j for j in journals}
        ordered = [journal_map[i] for i in ids if i in journal_map][::-1]

        return ordered
