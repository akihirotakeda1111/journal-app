from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from journal.serializers.evidence import (
    EvidenceInputSerializer,
    EvidenceOutputSerializer,
)
from journal.services.evidence import EvidenceService


class JournalEvidenceCreateAPIView(APIView):
    def post(self, request, journal_id):
        input = EvidenceInputSerializer(data=request.data)
        input.is_valid(raise_exception=True)

        evidence = EvidenceService.create(journal_id, input.validated_data["key"])

        output = EvidenceOutputSerializer(evidence)
        return Response(output.data, status=status.HTTP_201_CREATED)


class JournalEvidenceListAPIView(APIView):
    def get(self, request, journal_id):

        evidences = EvidenceService.list(journal_id)

        output = EvidenceOutputSerializer(evidences, many=True)
        return Response(output.data, status=status.HTTP_200_OK)
