from django.db.models import Sum, Q, Value, IntegerField
from django.db.models.functions import Coalesce
from management.models import Account
from journal.domain.constants import Side
from management.domain.constants import AccountType


class TrialBalanceService:

    @staticmethod
    def get(start_date, end_date) -> list[dict]:
        """勘定科目ごとに残高を集計"""

        # 仕訳日付のフィルタを作成
        date_filter = Q()
        if start_date:
            date_filter &= Q(journal_lines__journal__recorded_date__gte=start_date)
        if end_date:
            date_filter &= Q(journal_lines__journal__recorded_date__lte=end_date)

        # 勘定科目ごとに残高を集計
        accounts = Account.objects.annotate(
            net_total=Coalesce(
                Sum("journal_lines__amount", filter=date_filter),
                Value(0, output_field=IntegerField()),
                output_field=IntegerField(),
            )
        ).order_by("id")

        trial_balance = []
        for account in accounts:
            acc_type = account.type
            net_total = account.net_total

            # 貸借の判定
            if acc_type in [AccountType.ASSET, AccountType.EXPENSE]:
                balance = net_total
                normal_side = Side.DEBIT
            else:
                balance = -net_total
                normal_side = Side.CREDIT

            actual_side = (
                normal_side
                if balance >= 0
                else (Side.CREDIT if normal_side == Side.DEBIT else Side.DEBIT)
            )

            trial_balance.append(
                {
                    "account_id": account.id,
                    "account_name": account.name,
                    "account_type": acc_type,
                    "balance": abs(balance),
                    "side": actual_side,
                }
            )

        return trial_balance
