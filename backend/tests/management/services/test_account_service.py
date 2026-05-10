import pytest
from management.models import Account
from management.services.account import AccountService


def test_list_ordered(db, setup_accounts):
    """id の昇順で取得されること"""

    setup_accounts
    qs = AccountService.list()
    ids = list(qs.values_list("id", flat=True))

    assert ids == ["T01", "T02", "T03", "T04"]


def test_list_returns_empty_when_no_accounts(db):
    """勘定科目が存在しない場合は空のクエリセットが返ること"""

    # Account テーブルが空であること
    assert Account.objects.count() == 0

    qs = AccountService.list()
    assert list(qs) == []
