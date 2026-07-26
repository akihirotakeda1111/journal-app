from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from journal.models.evidence import Evidence
from utils.services.download import DownloadService


class EvidenceDownloadAPIView(APIView):
    def get(self, request, evidence_id):
        try:
            evidence = Evidence.objects.get(id=evidence_id)
        except Evidence.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        service = DownloadService()
        result = service.generate_presigned_get_url(evidence.key)

        return Response(result, status=status.HTTP_200_OK)
