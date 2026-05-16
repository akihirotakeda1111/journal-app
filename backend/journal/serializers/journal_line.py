from rest_framework import serializers
from journal.models import JournalLine
from journal.domain.constants import AmountRules, Side


class JournalLineInputSerializer(serializers.Serializer):
    side = serializers.ChoiceField(choices=Side.CHOICES)
    account_id = serializers.CharField(max_length=10)
    amount = serializers.IntegerField(
        min_value=AmountRules.MIN,
        max_value=AmountRules.MAX,
    )


class JournalLineOutputSerializer(serializers.ModelSerializer):
    side = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = JournalLine
        fields = ["account_id", "side", "amount"]

    def get_side(self, obj: JournalLine) -> str:
        """DBの符号から DEBIT / CREDIT へ変換"""
        return Side.DEBIT if obj.amount > 0 else Side.CREDIT

    def get_amount(self, obj: JournalLine) -> int:
        """DBの符号付き整数から絶対値へ変換"""
        return abs(obj.amount)
