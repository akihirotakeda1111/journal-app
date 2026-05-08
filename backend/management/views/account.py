from rest_framework import generics
from management.services.account import AccountService
from management.serializers.account import AccountOutputSerializer
from rest_framework.response import Response
from rest_framework import status


class AccountListAPIView(generics.ListAPIView):
    def get(self, request):
        accounts = AccountService.list()

        output = AccountOutputSerializer(accounts, many=True)

        return Response(output.data, status=status.HTTP_200_OK)
