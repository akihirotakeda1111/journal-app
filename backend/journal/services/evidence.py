from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from journal.models.evidence import Evidence
from journal.models.journal import Journal
from journal.exceptions.journal_exceptions import JournalNotFoundError, InvalidJournalIdError, EvidenceCreateError


class EvidenceService:

    @staticmethod
    @transaction.atomic
    def create(journal_id: str, key: str) -> Evidence:
        try:
            journal = Journal.objects.get(id=journal_id)
        except Journal.DoesNotExist:
            raise JournalNotFoundError(journal_id)
        except (ValueError, ValidationError):
            raise InvalidJournalIdError(journal_id)

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
        return Evidence.objects.filter(journal_id=journal_id).order_by("-uploaded_at")