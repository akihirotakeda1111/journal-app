from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.services.upload import UploadService
from utils.serializers.upload import UploadRequestSerializer


class UploadAPIView(APIView):
    serializer_class = UploadRequestSerializer
    service_class = UploadService

    def get_serializer_class(self):
        return self.serializer_class

    def get_service_class(self):
        return self.service_class

    def get_upload_metadata(self, validated_data: dict) -> dict:
        return {}

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        service = self.get_service_class()()
        result = service.generate_presigned_put_url(
            filename=validated_data["filename"],
            content_type=validated_data["content_type"],
            category=validated_data["category"],
            metadata=self.get_upload_metadata(validated_data),
        )

        return Response(result, status=status.HTTP_200_OK)
