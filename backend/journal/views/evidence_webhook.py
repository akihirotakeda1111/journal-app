import secrets
import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from journal.serializers.evidence import EvidenceOutputSerializer
from journal.serializers.evidence_webhook import EvidenceWebhookInputSerializer
from journal.services.evidence import EvidenceService

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class EvidenceWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def _is_authorized(self, request) -> bool:
        expected_secret = settings.WEBHOOK_SECRET
        if not expected_secret:
            return False

        auth_header = request.headers.get("Authorization", "")
        expected_header = f"Bearer {expected_secret}"
        return secrets.compare_digest(auth_header, expected_header)

    def post(self, request):
        if not self._is_authorized(request):
            logger.warning("Evidence webhook rejected: invalid or missing Authorization")
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = EvidenceWebhookInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bucket = serializer.validated_data["bucket"]
        key = serializer.validated_data["key"]

        try:
            evidence, created = EvidenceService.register_from_s3(bucket, key)
        except Exception:
            logger.exception(
                "Evidence webhook failed for s3://%s/%s",
                bucket,
                key,
            )
            raise

        output = EvidenceOutputSerializer(evidence)
        response_status = (
            status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

        return Response(output.data, status=response_status)
