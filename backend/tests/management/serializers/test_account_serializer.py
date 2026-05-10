import pytest
from management.models import Account
from management.serializers.account import AccountOutputSerializer


def test_account_output_serializer(db):
    """正常に出力されること"""

    account = Account.objects.create(
        id="T01",
        name="Test",
        type="ASSET",
    )

    serializer = AccountOutputSerializer(account)
    data = serializer.data

    assert data["id"] == "T01"
    assert data["name"] == "Test"
    assert data["type"] == "ASSET"
    assert set(data.keys()) == {"id", "name", "type"}
