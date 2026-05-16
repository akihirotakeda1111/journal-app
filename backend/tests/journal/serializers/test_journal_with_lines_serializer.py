import pytest
from journal.models import Journal, JournalLine
from journal.serializers.journal_with_lines import (
    JournalWithLinesInputSerializer,
    JournalWithLinesOutputSerializer,
)
from journal.domain.constants import JournalLineRules, JournalType, Side
from uuid import UUID
from datetime import date


def test_journal_with_lines_input_serializer_valid(setup_accounts):
    """借方と貸方の合計が一致している場合、バリデーションが通ること"""

    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
        ],
    }

    serializer = JournalWithLinesInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert "lines" in validated
    assert len(validated["lines"]) == 2


def test_journal_with_lines_input_serializer_valid_max_length(setup_accounts):
    """lines が最大行数までバリデーションが通ること"""

    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "side": Side.DEBIT, "amount": i}
            for i in range(JournalLineRules.MAX_ROW)
        ],
    }

    serializer = JournalWithLinesInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "lines" in serializer.errors


def test_journal_with_lines_input_serializer_invalid_unbalanced(setup_accounts):
    """借方と貸方の合計が一致しない場合、バリデーションエラーになること"""

    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 50, "side": Side.CREDIT},
        ],
    }

    serializer = JournalWithLinesInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors or "__all__" in serializer.errors


def test_journal_with_lines_input_serializer_empty_lines():
    """lines が空配列の場合、バリデーションエラーになること"""

    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [],
    }

    serializer = JournalWithLinesInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "lines" in serializer.errors


def test_journal_with_lines_input_serializer_max_length(setup_accounts):
    """lines が最大行数を超えた場合、バリデーションエラーになること"""

    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "side": Side.DEBIT, "amount": i}
            for i in range(JournalLineRules.MAX_ROW + 1)
        ],
    }

    serializer = JournalWithLinesInputSerializer(data=payload)

    assert not serializer.is_valid()
    assert "lines" in serializer.errors


def test_journal_with_lines_output_serializer_value(db, setup_accounts):
    """仕訳ヘッダーと仕訳明細を含めて返すこと"""

    asset, liability, expense, revenue = setup_accounts
    journal = Journal.objects.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        recorded_date=date(2026, 1, 1),
        description="test",
        type=JournalType.NORMAL,
    )

    journal1 = JournalLine.objects.create(
        journal=journal, account=asset, amount=200
    )  # DEBIT
    journal2 = JournalLine.objects.create(
        journal=journal, account=liability, amount=-200
    )  # CREDIT

    serializer = JournalWithLinesOutputSerializer(journal)
    data = serializer.data

    # 仕訳ヘッダーが含まれていること
    assert data["id"] == str(journal.id)
    assert data["recorded_date"] == "2026-01-01"
    assert data["description"] == "test"
    assert data["type"] == JournalType.NORMAL

    # 仕訳明細 が含まれていること
    assert "lines" in data
    assert isinstance(data["lines"], list)
    assert len(data["lines"]) == 2

    # 借方（正の値）は DEBIT、amount は絶対値
    line0 = data["lines"][0]
    assert line0["account_id"] == asset.id
    assert line0["side"] == Side.DEBIT
    assert line0["amount"] == 200

    # 貸方（負の値）は CREDIT、amount は絶対値
    line1 = data["lines"][1]
    assert line1["account_id"] == liability.id
    assert line1["side"] == Side.CREDIT
    assert line1["amount"] == 200


def test_journal_with_lines_output_serializer_field():
    """Meta.fields に 'lines' が追加されていること"""

    meta_fields = getattr(JournalWithLinesOutputSerializer.Meta, "fields", None)
    assert meta_fields is not None
    assert "lines" in meta_fields
