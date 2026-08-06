from django.db import transaction, IntegrityError

from journal.models.evidence import Evidence
from journal.models.journal import Journal
from journal.exceptions.journal_exceptions import (
    EvidenceCreateError,
    EvidenceMetadataMissingError,
    EvidenceNotFoundError,
    InvalidJournalIdError,
    JournalNotFoundError,
)
from utils.services.download import DownloadService
from utils.services.s3 import S3Service

JOURNAL_ID_METADATA_KEYS = ("journal-id", "journal_id")


class EvidenceService:

    @staticmethod
    def _extract_journal_id(metadata: dict) -> str | None:
        for key in JOURNAL_ID_METADATA_KEYS:
            value = metadata.get(key)
            if value:
                return value
        return None

    @staticmethod
    def _get_journal(journal_id):
        try:
            journal_uuid = Journal.to_uuid(journal_id)
        except (ValueError, TypeError):
            raise InvalidJournalIdError(str(journal_id))

        try:
            return Journal.objects.get(id=journal_uuid)
        except Journal.DoesNotExist:
            raise JournalNotFoundError(str(journal_id))

    @staticmethod
    @transaction.atomic
    def create(journal_id: str, key: str) -> Evidence:
        journal = EvidenceService._get_journal(journal_id)

        try:
            evidence = Evidence.objects.create(
                journal=journal,
                key=key,
            )
            return evidence
        except IntegrityError as e:
            raise EvidenceCreateError(key, str(e))

    @staticmethod
    @transaction.atomic
    def register_from_s3(bucket: str, key: str) -> tuple[Evidence, bool]:
        existing = Evidence.objects.filter(key=key).first()
        if existing:
            return existing, False

        metadata = S3Service().head_object_metadata(bucket, key)
        journal_id = EvidenceService._extract_journal_id(metadata)
        if not journal_id:
            raise EvidenceMetadataMissingError(key)

        journal = EvidenceService._get_journal(journal_id)

        try:
            evidence = Evidence.objects.create(
                journal=journal,
                key=key,
            )
            return evidence, True
        except IntegrityError:
            return Evidence.objects.get(key=key), False

    @staticmethod
    def list(journal_id: str):
        journal = EvidenceService._get_journal(journal_id)
        return Evidence.objects.filter(journal_id=journal.id).order_by("-uploaded_at")

    @staticmethod
    def get_download_url(evidence_id: int) -> dict:
        try:
            evidence = Evidence.objects.get(id=evidence_id)
        except Evidence.DoesNotExist:
            raise EvidenceNotFoundError(evidence_id)

        service = DownloadService()
        return service.generate_presigned_get_url(evidence.key)
