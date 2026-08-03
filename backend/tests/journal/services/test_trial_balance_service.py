import pytest
from management.models import Account
from journal.models import Journal, JournalLine
from journal.services.trial_balance import TrialBalanceService
from journal.domain.constants import AmountRules, JournalType, Side
from management.domain.constants import AccountType
from datetime import date, timedelta
from uuid import UUID


def test_trial_balance_get(db, setup_accounts):
    """各勘定項目ごとに残高と貸借の区分が正しく集計されること"""

    asset, liability, expense, revenue = setup_accounts

    # 基準日
    base_date = date(2026, 1, 1)

    # Journal を作成
    journal1 = Journal.objects.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        recorded_date=base_date,
        description="",
        type=JournalType.NORMAL,
    )
    # journal1: asset に借方 1000, liability に貸方 -1000
    JournalLine.objects.create(journal=journal1, account=asset, amount=1000)
    JournalLine.objects.create(journal=journal1, account=liability, amount=-1000)

    # journal2: expense に借方 300, revenue に貸方 -300
    journal2 = Journal.objects.create(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        recorded_date=base_date,
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal2, account=expense, amount=300)
    JournalLine.objects.create(journal=journal2, account=revenue, amount=-300)

    # journal3: asset に貸方に -200, liability に借方 200
    journal3 = Journal.objects.create(
        id=UUID("33333333-3333-3333-3333-333333333333"),
        recorded_date=base_date,
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal3, account=asset, amount=-200)
    JournalLine.objects.create(journal=journal3, account=liability, amount=200)

    # 集計実行
    tb = TrialBalanceService.get(None, None)
    tb_map = {row["account_id"]: row for row in tb}

    # ASSET: 1000 + (-200) = 800 -> DEBIT
    asset_row = tb_map[asset.id]
    assert asset_row["balance"] == 800
    assert asset_row["side"] == Side.DEBIT

    # LIABILITY: -1000 + 200 = -800 -> CREDIT
    liability_row = tb_map[liability.id]
    assert liability_row["balance"] == 800
    assert liability_row["side"] == Side.CREDIT

    # EXPENSE: 300 -> DEBIT
    expense_row = tb_map[expense.id]
    assert expense_row["balance"] == 300
    assert expense_row["side"] == Side.DEBIT

    # REVENUE: -300 -> CREDIT
    revenue_row = tb_map[revenue.id]
    assert revenue_row["balance"] == 300
    assert revenue_row["side"] == Side.CREDIT


def test_trial_balance_get_with_date_range(db, setup_accounts):
    """start_date / end_date を指定した場合、期間内の仕訳のみが集計されること"""

    asset, liability, expense, revenue = setup_accounts
    start_date = date(2026, 1, 1)
    end_date = date(2026, 1, 31)

    # 期間外の仕訳（start_date - 1日）
    journal1 = Journal.objects.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        recorded_date=start_date - timedelta(days=1),
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal1, account=asset, amount=500)
    JournalLine.objects.create(journal=journal1, account=liability, amount=-500)

    # 期間内の仕訳（start_date）
    journal2 = Journal.objects.create(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        recorded_date=start_date,
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal2, account=asset, amount=300)
    JournalLine.objects.create(journal=journal2, account=liability, amount=-300)

    # 期間内の仕訳（end_date）
    journal3 = Journal.objects.create(
        id=UUID("33333333-3333-3333-3333-333333333333"),
        recorded_date=end_date,
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal3, account=asset, amount=700)
    JournalLine.objects.create(journal=journal3, account=liability, amount=-700)

    # 期間外の仕訳（end_date + 1日）
    journal4 = Journal.objects.create(
        id=UUID("44444444-4444-4444-4444-444444444444"),
        recorded_date=end_date + timedelta(days=1),
        description="",
        type=JournalType.NORMAL,
    )
    JournalLine.objects.create(journal=journal4, account=expense, amount=900)
    JournalLine.objects.create(journal=journal4, account=revenue, amount=-900)

    # 集計実行（期間指定）
    tb = TrialBalanceService.get(start_date, end_date)
    tb_map = {r["account_id"]: r for r in tb}

    # 期間内合計 300 + 700 = 1000 -> balance 1000, side DEBIT
    assert tb_map[asset.id]["balance"] == 1000
    assert tb_map[asset.id]["side"] == Side.DEBIT

    # 期間内合計 -300 + (-700) = -1000 -> balance 1000, side CREDIT
    assert tb_map[liability.id]["balance"] == 1000
    assert tb_map[liability.id]["side"] == Side.CREDIT

    # 期間内の仕訳がない場合は balance 0, side DEBIT（デフォルト）
    assert tb_map[expense.id]["balance"] == 0
    assert tb_map[expense.id]["side"] == Side.DEBIT


def test_trial_balance_get_ordered(db, setup_accounts):
    """戻り値の順序が Account.id の昇順であること"""

    asset, liability, expense, revenue = setup_accounts

    # 仕訳を作成
    for i, acc in enumerate([asset, liability, expense, revenue]):
        j = Journal.objects.create(
            id=UUID(f"11111111-1111-1111-1111-{i:012d}"),
            recorded_date=date(2026, 1, 10 + i),
            description="Test",
            type=JournalType.NORMAL,
        )
        amt = 100 * (i + 1)
        JournalLine.objects.create(
            journal=j,
            account=acc,
            amount=(
                amt
                if acc.type == AccountType.ASSET or acc.type == AccountType.EXPENSE
                else -amt
            ),
        )

    tb = TrialBalanceService.get(None, None)
    ids = [row["account_id"] for row in tb]

    # Account.objects.order_by('id') と同じ順序で返っていること
    expected_ids = list(Account.objects.order_by("id").values_list("id", flat=True))
    assert ids == list(expected_ids)


def test_trial_balance_get_max_amount_record(db, setup_accounts):
    """金額の最大値を最大レコード投入しても正しく集計されること"""

    asset, liability, expense, revenue = setup_accounts

    MAX_AMOUNT = AmountRules.MAX
    RECORD_COUNT = 100

    # Journal を大量生成
    for i in range(RECORD_COUNT):
        j = Journal.objects.create(
            id=UUID(f"aaaaaaaa-aaaa-aaaa-aaaa-{i:012d}"),
            recorded_date=date(2026, 1, 1),
            description=f"max test {i}",
            type=JournalType.NORMAL,
        )
        # asset に借方（正）
        JournalLine.objects.create(journal=j, account=asset, amount=MAX_AMOUNT)
        # liability に貸方（負）
        JournalLine.objects.create(journal=j, account=liability, amount=-MAX_AMOUNT)

    # 集計実行
    tb = TrialBalanceService.get(None, None)
    tb_map = {row["account_id"]: row for row in tb}

    # 期待値：MAX_AMOUNT × RECORD_COUNT
    expected_total = MAX_AMOUNT * RECORD_COUNT

    # ASSET → 借方（正）
    asset_row = tb_map[asset.id]
    assert asset_row["balance"] == expected_total
    assert asset_row["side"] == Side.DEBIT

    # LIABILITY → 貸方（負）
    liability_row = tb_map[liability.id]
    assert liability_row["balance"] == expected_total
    assert liability_row["side"] == Side.CREDIT


def test_trial_balance_invalid_date_format():
    """不正な日付形式の場合、ApplicationValidationErrorが発生すること"""
    from utils.exceptions.application_errors import ApplicationValidationError

    with pytest.raises(ApplicationValidationError) as excinfo:
        TrialBalanceService.get("2026/01/01", None)

    assert excinfo.value.code == "INVALID_DATE_FORMAT"


def test_trial_balance_invalid_date_range():
    """start_date が end_date より後の場合、ApplicationValidationErrorが発生すること"""
    from utils.exceptions.application_errors import ApplicationValidationError

    with pytest.raises(ApplicationValidationError) as excinfo:
        TrialBalanceService.get("2026-02-01", "2026-01-01")

    assert excinfo.value.code == "INVALID_DATE_RANGE"

