from rest_framework import serializers
from journal.models.evidence import Evidence


class EvidenceInputSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)


class EvidenceOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ["id", "key", "uploaded_at"]
