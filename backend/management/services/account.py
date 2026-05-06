from django.db import transaction, IntegrityError
from django.db.models import OuterRef, Exists
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from ..models import Account
from ..serializers.account import AccountOutputSerializer


class AccountService:

    @staticmethod
    def list():
        """勘定科目を全権取得"""
        accounts = Account.objects.all()
        serializer = AccountOutputSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
