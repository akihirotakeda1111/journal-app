from rest_framework import serializers
from ..models import Account


class AccountOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "type"]
