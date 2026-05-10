import pytest
from management.models import Account


def test_account_list_view(db, client, setup_accounts):
    """勘定科目の一覧が正しく返ること"""

    setup_accounts
    response = client.get("/api/management/account/list/")
    data = response.json()

    assert response.status_code == 200
    assert [row["id"] for row in data] == ["T01", "T02", "T03", "T04"]
    assert set(data[0].keys()) == {"id", "name", "type"}


def test_account_list_view_empty(db, client):
    """勘定科目が存在しない場合、空配列が返ること"""

    assert Account.objects.count() == 0

    response = client.get("/api/management/account/list/")

    assert response.status_code == 200
    assert response.json() == []
