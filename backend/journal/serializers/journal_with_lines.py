from rest_framework import serializers
from journal.serializers.journal import JournalInputSerializer, JournalOutputSerializer
from journal.serializers.journal_line import (
    JournalLineInputSerializer,
    JournalLineOutputSerializer,
)
from journal.domain.constants import JournalLineRules


class JournalWithLinesInputSerializer(JournalInputSerializer):
    lines = JournalLineInputSerializer(
        many=True, allow_empty=False, max_length=JournalLineRules.MAX_ROW
    )

    def validate(self, data):
        """貸借合計の完全一致を検証"""
        lines = data.get("lines", [])
        debit_sum = sum(line["amount"] for line in lines if line["side"] == "DEBIT")
        credit_sum = sum(line["amount"] for line in lines if line["side"] == "CREDIT")

        if debit_sum != credit_sum:
            raise serializers.ValidationError(
                "借方と貸方の合計金額が一致していません。"
            )
        return data


class JournalWithLinesOutputSerializer(JournalOutputSerializer):
    lines = JournalLineOutputSerializer(many=True, read_only=True)

    class Meta(JournalOutputSerializer.Meta):
        fields = JournalOutputSerializer.Meta.fields + ["lines"]
