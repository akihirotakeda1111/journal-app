from rest_framework import generics
from ..services.account import AccountService


class AccountListAPIView(generics.ListAPIView):
    def get(self, request):
        return AccountService.list()
