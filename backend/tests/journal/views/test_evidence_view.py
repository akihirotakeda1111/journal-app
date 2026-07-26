import pytest
from unittest.mock import patch
from rest_framework import status
from uuid import UUID
from journal.models import Evidence, Journal
from django.utils import timezone

BASE_CREATE = "/api/journal/evidence/{journal_id}/"
BASE_LIST = "/api/journal/evidence/list/{journal_id}/"


class DummyInputSerializer:
    def __init__(self, data=None):
        self._data = data
        self.validated_data = None

    def is_valid(self, raise_exception=False):
        self.validated_data = self._data or {}
        return True


class DummyOutputSerializer:
    def __init__(self, obj, many=False):
        self.obj = obj
        self.many = many

    @property
    def data(self):
        return self.obj


def test_evidence_create_view(client, db):
    """証憑登録リクエストが正常に処理され、レスポンスが返ること"""

    journal_id_str = "11111111-1111-1111-1111-111111111111"
    journal_id_uuid = UUID(journal_id_str)

    payload = {
        "key": "evidence/test.pdf",
    }

    journal = Journal.objects.create(
        id=journal_id_str,
        recorded_date=timezone.now().date(),
    )

    fake_evidence = Evidence(
        id=1,
        journal=journal,
        key="evidence/test.pdf",
        uploaded_at=timezone.now(),
    )

    input_path = "journal.serializers.evidence.EvidenceInputSerializer"
    service_path = "journal.services.evidence.EvidenceService.create"

    with patch(input_path, new=DummyInputSerializer), patch(
        service_path, return_value=fake_evidence
    ) as mock_create:
        resp = client.post(
            BASE_CREATE.format(journal_id=journal_id_str), payload, format="json"
        )

    mock_create.assert_called_once_with(journal_id_uuid, payload["key"])
    assert resp.status_code == status.HTTP_201_CREATED

    expected = {
        "id": 1,
        "key": "evidence/test.pdf",
        "uploadedAt": fake_evidence.uploaded_at.isoformat().replace("+00:00", "Z"),
    }
    assert resp.json() == expected


def test_evidence_list_view(client, db):
    """証憑一覧取得リクエストが正常に処理され、レスポンスが返ること"""

    journal_id_str = "11111111-1111-1111-1111-111111111111"
    journal_id_uuid = UUID(journal_id_str)

    fake_list = [
        {
            "id": 1,
            "key": "evidence/a.pdf",
            # "uploadedAt": "2026-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "key": "evidence/b.pdf",
            # "uploadedAt": "2026-01-02T00:00:00Z",
        },
    ]

    output_path = "journal.serializers.evidence.EvidenceOutputSerializer"
    service_path = "journal.services.evidence.EvidenceService.list"

    with patch(output_path, new=DummyOutputSerializer), patch(
        service_path, return_value=fake_list
    ) as mock_list:
        resp = client.get(BASE_LIST.format(journal_id=journal_id_str))

    mock_list.assert_called_once_with(journal_id_uuid)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_list
