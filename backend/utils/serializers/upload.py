from rest_framework import serializers


class UploadRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()
    content_type = serializers.CharField()
    category = serializers.CharField()
