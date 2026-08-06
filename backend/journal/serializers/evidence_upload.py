from rest_framework import serializers

from utils.serializers.upload import UploadRequestSerializer


class EvidenceUploadRequestSerializer(UploadRequestSerializer):
    journal_id = serializers.UUIDField()
