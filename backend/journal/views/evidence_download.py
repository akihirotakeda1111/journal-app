from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from journal.services.evidence import EvidenceService


class EvidenceDownloadAPIView(APIView):
    def get(self, request, evidence_id):
        result = EvidenceService.get_download_url(evidence_id)
        return Response(result, status=status.HTTP_200_OK)
