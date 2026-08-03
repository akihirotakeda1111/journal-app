import pytest
from unittest.mock import patch
from django.utils import timezone
from rest_framework import status

from journal.models import Evidence, Journal

BASE_DOWNLOAD = "/api/journal/evidence/download/{evidence_id}/"


def test_evidence_download_success(client, db):
    """証憑ダウンロードURLが正常に返ること"""
    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        recorded_date=timezone.now().date(),
    )
    evidence = Evidence.objects.create(journal=journal, key="evidence/test.pdf")
    fake_result = {"url": "https://example.com/presigned"}

    with patch("journal.services.evidence.DownloadService") as mock_service:
        mock_service.return_value.generate_presigned_get_url.return_value = {
            "url": "https://example.com/presigned"
        }
        resp = client.get(BASE_DOWNLOAD.format(evidence_id=evidence.id))

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_result


def test_evidence_download_not_found(client, db):
    """存在しない証憑IDで404と標準エラー形式が返ること"""
    resp = client.get(BASE_DOWNLOAD.format(evidence_id=99999))

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    body = resp.json()
    assert body["error"]["code"] == "EVIDENCE_NOT_FOUND"
    assert "99999" in body["error"]["message"]
