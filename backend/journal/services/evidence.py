from django.db import transaction
from journal.models.evidence import Evidence
from journal.models.journal import Journal


class EvidenceService:

    @staticmethod
    @transaction.atomic
    def create(journal_id: str, key: str) -> Evidence:
        journal = Journal.objects.get(id=journal_id)

        evidence = Evidence.objects.create(
            journal=journal,
            key=key,
        )

        return evidence

    @staticmethod
    def list(journal_id: str):
        return Evidence.objects.filter(journal_id=journal_id).order_by("-uploaded_at")
