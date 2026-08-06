import pytest
from django.utils import timezone
from unittest.mock import patch

from journal.models.journal import Journal
from journal.models.evidence import Evidence
from journal.services.evidence import EvidenceService
from journal.exceptions.journal_exceptions import EvidenceMetadataMissingError


def test_register_from_s3_creates_evidence(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )

    with patch("journal.services.evidence.S3Service") as mock_s3:
        mock_s3.return_value.head_object_metadata.return_value = {
            "journal-id": str(journal.id),
        }

        evidence, created = EvidenceService.register_from_s3(
            "test-bucket",
            "evidence/new.pdf",
        )

    assert created is True
    assert evidence.key == "evidence/new.pdf"
    assert evidence.journal_id == Journal.to_uuid(journal.id)


def test_register_from_s3_skips_existing_key(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )
    existing = Evidence.objects.create(
        journal=journal,
        key="evidence/existing.pdf",
    )

    with patch("journal.services.evidence.S3Service") as mock_s3:
        evidence, created = EvidenceService.register_from_s3(
            "test-bucket",
            "evidence/existing.pdf",
        )

    mock_s3.assert_not_called()
    assert created is False
    assert evidence.id == existing.id


def test_register_from_s3_missing_metadata(db):
    with patch("journal.services.evidence.S3Service") as mock_s3:
        mock_s3.return_value.head_object_metadata.return_value = {}

        with pytest.raises(EvidenceMetadataMissingError):
            EvidenceService.register_from_s3(
                "test-bucket",
                "evidence/no-metadata.pdf",
            )


def test_register_from_s3_handles_integrity_error_race(db):
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )
    existing = Evidence.objects.create(
        journal=journal,
        key="evidence/race.pdf",
    )

    with patch("journal.services.evidence.S3Service") as mock_s3, patch(
        "journal.models.evidence.Evidence.objects.create"
    ) as mock_create:
        from django.db import IntegrityError

        mock_s3.return_value.head_object_metadata.return_value = {
            "journal-id": str(journal.id),
        }
        mock_create.side_effect = IntegrityError("duplicate key")

        evidence, created = EvidenceService.register_from_s3(
            "test-bucket",
            "evidence/race.pdf",
        )

    assert created is False
    assert evidence.id == existing.id
