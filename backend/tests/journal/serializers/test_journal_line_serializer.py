import pytest
from journal.serializers.journal_line import (
    JournalLineInputSerializer,
    JournalLineOutputSerializer,
)
from journal.models import Journal, JournalLine
from uuid import UUID
from datetime import date


def test_journal_line_input_serializer_valid():
    """正常にバリデーションが通ること"""

    payload = {"side": "DEBIT", "account_id": "T01", "amount": 1}

    serializer = JournalLineInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert validated["side"] == "DEBIT"
    assert validated["account_id"] == "T01"
    assert validated["amount"] == 1


@pytest.mark.parametrize("invalid_side", ["INVALID", "", None])
def test_journal_line_input_serializer_invalid_side(invalid_side):
    """side は DEBIT/CREDIT 以外の場合、バリデーションエラーになること"""

    payload = {"side": invalid_side, "account_id": "T01", "amount": 10}

    serializer = JournalLineInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "side" in serializer.errors


@pytest.mark.parametrize("invalid_amount", [0, -1, None])
def test_journal_line_input_serializer_invalid_amount(invalid_amount):
    """amount は 1 未満の場合、バリデーションエラーになること"""

    payload = {"side": "DEBIT", "account_id": "T01", "amount": invalid_amount}

    serializer = JournalLineInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "amount" in serializer.errors


def test_journal_line_input_serializer_account_id_max_length():
    """account_id の max_length=10 を超えるとバリデーションエラーになること"""

    long_id = "A" * 11
    payload = {"side": "DEBIT", "account_id": long_id, "amount": 10}

    serializer = JournalLineInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "account_id" in serializer.errors


def test_journal_line_output_serializer(db, setup_accounts):
    """
    amount の符号に応じて side が DEBIT/CREDIT に変換されること
    amount は絶対値に変換されること
    """

    asset, liability, expense, revenue = setup_accounts
    journal = Journal.objects.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        recorded_date=date(2026, 1, 1),
        description="h",
        type="NORMAL",
    )

    # 借方（正の値）
    journal_debit = JournalLine.objects.create(
        journal=journal, account=asset, amount=150
    )
    out_debit = JournalLineOutputSerializer(journal_debit).data
    assert out_debit["account_id"] == asset.id
    assert out_debit["side"] == "DEBIT"
    assert out_debit["amount"] == 150

    # 貸方（負の値）
    journal_credit = JournalLine.objects.create(
        journal=journal, account=liability, amount=-150
    )
    out_credit = JournalLineOutputSerializer(journal_credit).data
    assert out_credit["account_id"] == liability.id
    assert out_credit["side"] == "CREDIT"
    assert out_credit["amount"] == 150
