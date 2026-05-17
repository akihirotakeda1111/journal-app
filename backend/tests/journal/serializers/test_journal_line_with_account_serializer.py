import pytest
from uuid import UUID
from datetime import date
from journal.serializers.journal_line_with_account import (
    JournalLineWithAccountSerializer,
)
from journal.models import JournalLine
from journal.models import Journal, JournalLine
from journal.domain.constants import JournalType, Side


def test_journal_line_with_account_serializer(db, setup_accounts):
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
        amount=1000,
    )

    serializer = JournalLineWithAccountSerializer(line)
    data = serializer.data

    # 継承クラスの値が正常に設定されること
    assert data["account_id"] == asset.id
    assert data["side"] == Side.DEBIT
    assert data["amount"] == 1000

    # account が設定されること
    assert data["account"] == {
        "id": asset.id,
        "name": asset.name,
        "type": asset.type,
    }
