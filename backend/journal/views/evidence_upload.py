from utils.views.upload import UploadAPIView

from journal.serializers.evidence_upload import EvidenceUploadRequestSerializer


class EvidenceUploadAPIView(UploadAPIView):
    serializer_class = EvidenceUploadRequestSerializer

    def get_upload_metadata(self, validated_data: dict) -> dict:
        return {"journal_id": str(validated_data["journal_id"])}
