import pytest
from uuid import UUID
from datetime import date
from journal.models import Journal, JournalLine
from journal.serializers.journal_with_lines_and_account import (
    JournalWithLinesAndAccountSerializer,
)
from journal.domain.constants import JournalType, Side


def test_journal_with_lines_and_account_serializer(db, setup_accounts):
    """仕訳明細に勘定科目が紐づいたデータ変換が行えること"""

    asset, liability, expense, revenue = setup_accounts
    journal = Journal.objects.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        recorded_date=date(2026, 1, 1),
        description="Test",
        type=JournalType.NORMAL,
    )

    line = JournalLine.objects.create(
        journal=journal,
        account=asset,
        account_id=asset.id,
        amount=1000,
    )

    serializer = JournalWithLinesAndAccountSerializer(journal)
    data = serializer.data

    # 継承クラスの値が正常に設定されること
    assert data["id"] == str(journal.id)
    assert data["recorded_date"] == "2026-01-01"
    assert data["description"] == "Test"
    assert data["type"] == JournalType.NORMAL

    assert len(data["lines"]) == 1
    line_data = data["lines"][0]

    assert line_data["account_id"] == asset.id
    assert line_data["side"] == Side.DEBIT
    assert line_data["amount"] == 1000

    # account が設定されること
    assert line_data["account"] == {
        "id": asset.id,
        "name": asset.name,
        "type": asset.type,
    }
