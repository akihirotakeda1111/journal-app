from ..models import Account


class AccountService:

    @staticmethod
    def list():
        """勘定科目を全件取得"""
        accounts = Account.objects.order_by("id")
        return accounts
