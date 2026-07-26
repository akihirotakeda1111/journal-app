from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.services.upload import UploadService
from utils.serializers.upload import UploadRequestSerializer


class UploadAPIView(APIView):
    def post(self, request):
        serializer = UploadRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename = serializer.validated_data["filename"]
        content_type = serializer.validated_data["content_type"]
        category = serializer.validated_data["category"]

        service = UploadService()
        result = service.generate_presigned_put_url(filename, content_type, category)

        return Response(result, status=status.HTTP_200_OK)
