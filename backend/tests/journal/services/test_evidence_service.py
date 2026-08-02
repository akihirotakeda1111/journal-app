import pytest
from django.utils import timezone
from unittest.mock import patch
from django.db import IntegrityError

from journal.models.journal import Journal
from journal.models.evidence import Evidence
from journal.services.evidence import EvidenceService
from journal.exceptions.journal_exceptions import (
    JournalNotFoundError,
    InvalidJournalIdError,
    EvidenceCreateError,
)


def test_create_success(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )

    evidence = EvidenceService.create(
        journal_id="11111111-1111-1111-1111-111111111111", key="evidence/test.pdf"
    )

    assert evidence.id is not None
    assert evidence.key == "evidence/test.pdf"
    assert evidence.journal_id == Journal.to_uuid(
        "11111111-1111-1111-1111-111111111111"
    )


def test_create_invalid_journal(db):
    invalid_uuid = "11111111-1111-1111-1111-111111111112"

    with pytest.raises(JournalNotFoundError):
        EvidenceService.create(invalid_uuid, "evidence/test.pdf")


def test_create_invalid_uuid(db):
    invalid_uuid = "not-a-uuid"

    with pytest.raises(InvalidJournalIdError):
        EvidenceService.create(invalid_uuid, "evidence/test.pdf")


def test_create_integrity_error(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )

    with patch("journal.models.evidence.Evidence.objects.create") as mocked_create:
        mocked_create.side_effect = IntegrityError("Mocked IntegrityError")

        with pytest.raises(EvidenceCreateError) as excinfo:
            EvidenceService.create(
                journal_id="11111111-1111-1111-1111-111111111111",
                key="evidence/test.pdf",
            )

        assert "Mocked IntegrityError" in str(excinfo.value)
        assert excinfo.value.code == "EVIDENCE_CREATE_FAILED"


def test_list(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )

    e1 = Evidence.objects.create(
        journal=journal,
        key="evidence/a.pdf",
        uploaded_at=timezone.now(),
    )
    e2 = Evidence.objects.create(
        journal=journal,
        key="evidence/b.pdf",
        uploaded_at=timezone.now() + timezone.timedelta(seconds=10),
    )

    items = EvidenceService.list("11111111-1111-1111-1111-111111111111")

    assert list(items) == [e2, e1]


def test_list_other_journal_excluded(db):
    j1 = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )
    j2 = Journal.objects.create(
        id="22222222-2222-2222-2222-222222222222",
        description="test2",
        recorded_date=timezone.now(),
    )

    Evidence.objects.create(journal=j1, key="evidence/a.pdf")
    Evidence.objects.create(journal=j2, key="evidence/b.pdf")

    items = EvidenceService.list("11111111-1111-1111-1111-111111111111")

    assert len(items) == 1
    assert items[0].journal_id == Journal.to_uuid(
        "11111111-1111-1111-1111-111111111111"
    )
