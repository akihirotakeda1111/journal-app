from rest_framework import serializers
from journal.models import Journal


class JournalInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()  # フロントエンドで発番
    recorded_date = serializers.DateField()
    description = serializers.CharField(required=False, allow_blank=True)


class JournalOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["id", "recorded_date", "description", "type"]
