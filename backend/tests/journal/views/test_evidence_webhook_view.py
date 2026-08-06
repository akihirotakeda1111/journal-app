import pytest
from django.test import override_settings
from django.utils import timezone
from rest_framework import status
from unittest.mock import patch

from journal.models.journal import Journal
from journal.models.evidence import Evidence


BASE_WEBHOOK = "/api/journal/evidence/webhook/"
WEBHOOK_SECRET = "test-webhook-secret"


@pytest.fixture
def journal(db):
    return Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        description="test",
        recorded_date=timezone.now(),
    )


@override_settings(WEBHOOK_SECRET=WEBHOOK_SECRET)
def test_evidence_webhook_creates_evidence(client, journal):
    payload = {
        "bucket": "test-bucket",
        "key": "evidence/new.pdf",
    }

    with patch("journal.services.evidence.S3Service") as mock_s3:
        mock_s3.return_value.head_object_metadata.return_value = {
            "journal-id": str(journal.id),
        }

        resp = client.post(
            BASE_WEBHOOK,
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {WEBHOOK_SECRET}",
        )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["key"] == "evidence/new.pdf"
    assert Evidence.objects.filter(key="evidence/new.pdf").exists()


@override_settings(WEBHOOK_SECRET=WEBHOOK_SECRET)
def test_evidence_webhook_returns_200_for_existing_key(client, journal):
    Evidence.objects.create(journal=journal, key="evidence/existing.pdf")
    payload = {
        "bucket": "test-bucket",
        "key": "evidence/existing.pdf",
    }

    with patch("journal.services.evidence.S3Service") as mock_s3:
        resp = client.post(
            BASE_WEBHOOK,
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {WEBHOOK_SECRET}",
        )

    mock_s3.assert_not_called()
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["key"] == "evidence/existing.pdf"


@override_settings(WEBHOOK_SECRET=WEBHOOK_SECRET)
def test_evidence_webhook_rejects_invalid_secret(client):
    payload = {
        "bucket": "test-bucket",
        "key": "evidence/new.pdf",
    }

    resp = client.post(
        BASE_WEBHOOK,
        payload,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer wrong-secret",
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN


@override_settings(WEBHOOK_SECRET=WEBHOOK_SECRET)
def test_evidence_webhook_rejects_missing_authorization(client):
    payload = {
        "bucket": "test-bucket",
        "key": "evidence/new.pdf",
    }

    resp = client.post(
        BASE_WEBHOOK,
        payload,
        content_type="application/json",
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN
