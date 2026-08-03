from datetime import date, datetime

from django.db.models import Sum, Q, Value, IntegerField
from django.db.models.functions import Coalesce

from management.models import Account
from journal.domain.constants import Side
from management.domain.constants import AccountType
from utils.exceptions.application_errors import ApplicationValidationError


class TrialBalanceService:

    @staticmethod
    def _parse_date(value, field_name: str) -> date | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ApplicationValidationError(
                f"{field_name} must be in YYYY-MM-DD format.",
                code="INVALID_DATE_FORMAT",
            )

    @staticmethod
    def get(start_date, end_date) -> list[dict]:
        """勘定科目ごとに残高を集計"""
        parsed_start = TrialBalanceService._parse_date(start_date, "start_date")
        parsed_end = TrialBalanceService._parse_date(end_date, "end_date")

        if parsed_start and parsed_end and parsed_start > parsed_end:
            raise ApplicationValidationError(
                "start_date must be before or equal to end_date.",
                code="INVALID_DATE_RANGE",
            )

        date_filter = Q()
        if parsed_start:
            date_filter &= Q(journal_lines__journal__recorded_date__gte=parsed_start)
        if parsed_end:
            date_filter &= Q(journal_lines__journal__recorded_date__lte=parsed_end)

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
