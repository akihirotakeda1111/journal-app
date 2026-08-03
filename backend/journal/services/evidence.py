from django.db import transaction, IntegrityError

from journal.models.evidence import Evidence
from journal.models.journal import Journal
from journal.exceptions.journal_exceptions import (
    EvidenceCreateError,
    EvidenceNotFoundError,
    InvalidJournalIdError,
    JournalNotFoundError,
)
from utils.services.download import DownloadService


class EvidenceService:

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
