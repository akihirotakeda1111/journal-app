import pytest
from rest_framework.test import APIClient
from management.models import Account


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def setup_accounts(db):
    """
    テスト用の勘定科目をセットアップ
    - ASSET: T01
    - LIABILITY: T03
    - EXPENSE: T04
    - REVENUE: T02
    """
    asset = Account.objects.create(id="T01", name="A", type="ASSET")
    liability = Account.objects.create(id="T03", name="B", type="LIABILITY")
    expense = Account.objects.create(id="T04", name="C", type="EXPENSE")
    revenue = Account.objects.create(id="T02", name="D", type="REVENUE")
    return asset, liability, expense, revenue
