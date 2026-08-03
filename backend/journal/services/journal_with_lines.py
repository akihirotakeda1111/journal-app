from django.db import transaction, IntegrityError
from django.db.models import OuterRef, Exists
from journal.models import Journal, JournalLine
from journal.domain.constants import AmountRules, JournalType, Side
from journal.exceptions.journal_exceptions import (
    CancelAlreadyExistsError,
    JournalAlreadyExistsError,
    JournalAlreadyModifiedError,
    JournalNotFoundError,
)
from utils.exceptions.application_errors import ApplicationValidationError
from uuid6 import uuid7


class _CancelJournalConflictError(Exception):
    """逆仕訳ヘッダー作成時のOneToOne制約違反（内部用）"""


class JournalWithLinesService:

    @staticmethod
    def _clean(data):
        """共通の内部バリデーションと正規化処理"""

        if "id" not in data:
            raise ApplicationValidationError("id is required")
        data["id"] = Journal.to_uuid(data["id"])

        if "recorded_date" not in data:
            raise ApplicationValidationError("recorded_date is required")
        data["recorded_date"] = Journal.to_date(data["recorded_date"])

        lines = data.get("lines")
        if not lines:
            raise ApplicationValidationError("lines must contain at least one item")

        for idx, line in enumerate(lines):
            if "account_id" not in line:
                raise ApplicationValidationError(
                    f"lines[{idx}].account_id is required"
                )

            if "amount" not in line:
                raise ApplicationValidationError(f"lines[{idx}].amount is required")
            else:
                if not (AmountRules.MIN <= line["amount"] <= AmountRules.MAX):
                    raise ApplicationValidationError(
                        f"lines[{idx}].amount must be between {AmountRules.MIN} and {AmountRules.MAX}"
                    )

            if "side" not in line:
                raise ApplicationValidationError(f"lines[{idx}].side is required")

            if line["side"] not in (Side.DEBIT, Side.CREDIT):
                raise ApplicationValidationError(
                    f"lines[{idx}].side must be {Side.DEBIT} or {Side.CREDIT}"
                )

        return data

    @staticmethod
    def _create_cancel_journal(original_journal: Journal) -> Journal:
        """元仕訳から逆仕訳を作成して返す"""

        try:
            cancel_journal = Journal.objects.create(
                id=uuid7(),
                recorded_date=original_journal.recorded_date,
                description=f"【取消】 {original_journal.description}",
                type=JournalType.CANCEL,
                original_journal=original_journal,
            )
        except IntegrityError as exc:
            raise _CancelJournalConflictError from exc

        # 明細（逆仕訳）を作成
        cancel_lines = [
            JournalLine(
                journal=cancel_journal,
                account_id=line.account_id,
                amount=-line.amount,
            )
            for line in original_journal.lines.all()
        ]
        JournalLine.objects.bulk_create(cancel_lines)

        return cancel_journal

    @staticmethod
    @transaction.atomic
    def create(data):
        data = JournalWithLinesService._clean(data)
        journal_id = data["id"]

        # すでに同じUUIDが存在する場合
        if Journal.objects.filter(id=journal_id).exists():
            raise JournalAlreadyExistsError(journal_id)

        try:
            journal = Journal.objects.create(
                id=journal_id,
                recorded_date=data["recorded_date"],
                description=data.get("description", ""),
                type=JournalType.NORMAL,
            )
        except IntegrityError:
            # 同時リクエストによるUUID重複のみドメイン例外へ変換
            if Journal.objects.filter(id=journal_id).exists():
                raise JournalAlreadyExistsError(journal_id)
            raise

        lines_to_create = []
        for line in data["lines"]:
            amount = (
                line["amount"] if line["side"] == Side.DEBIT else -line["amount"]
            )
            lines_to_create.append(
                JournalLine(
                    journal=journal,
                    account_id=line["account_id"],
                    amount=amount,
                )
            )

        JournalLine.objects.bulk_create(lines_to_create)

        return journal

    @staticmethod
    @transaction.atomic
    def cancel(original_journal_id: str) -> Journal:
        """逆仕訳の作成"""

        try:
            original_journal = (
                Journal.objects.select_for_update()
                .prefetch_related("lines")
                .get(id=original_journal_id)
            )
        except Journal.DoesNotExist:
            raise JournalNotFoundError(str(original_journal_id))

        try:
            return JournalWithLinesService._create_cancel_journal(original_journal)
        except _CancelJournalConflictError:
            raise CancelAlreadyExistsError(str(original_journal_id))

    @staticmethod
    @transaction.atomic
    def revise(original_journal_id: str, new_journal_data: dict) -> Journal:
        """逆仕訳、訂正仕訳の作成"""
        new_journal_data = JournalWithLinesService._clean(new_journal_data)

        try:
            original_journal = (
                Journal.objects.select_for_update()
                .prefetch_related("lines")
                .get(id=original_journal_id)
            )
        except Journal.DoesNotExist:
            raise JournalNotFoundError(str(original_journal_id))

        try:
            cancel_journal = JournalWithLinesService._create_cancel_journal(
                original_journal
            )
        except _CancelJournalConflictError:
            raise JournalAlreadyModifiedError(str(original_journal_id))

        new_journal_id = new_journal_data["id"]
        new_journal = Journal.objects.create(
            id=new_journal_id,
            recorded_date=new_journal_data["recorded_date"],
            description=new_journal_data.get("description", ""),
            type=JournalType.NORMAL,
            original_journal=cancel_journal,
        )

        new_lines = []
        for line in new_journal_data["lines"]:
            amount = (
                line["amount"] if line["side"] == Side.DEBIT else -line["amount"]
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

    @staticmethod
    def list():
        """最新の正常仕訳のみを取得する"""
        has_child = Journal.objects.filter(original_journal_id=OuterRef("id"))

        journals = (
            Journal.objects.filter(type=JournalType.NORMAL)
            .filter(~Exists(has_child))
            .prefetch_related("lines")
            .order_by("-recorded_date", "-created_at")
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
        journals = Journal.objects.filter(id__in=ids).prefetch_related(
            "lines", "lines__account"
        )

        # 古い順に並び替え
        journal_map = {j.id: j for j in journals}
        ordered = [journal_map[i] for i in ids if i in journal_map][::-1]

        return ordered
