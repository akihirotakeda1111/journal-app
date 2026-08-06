from rest_framework import serializers


class EvidenceWebhookInputSerializer(serializers.Serializer):
    bucket = serializers.CharField(max_length=255)
    key = serializers.CharField(max_length=255)
