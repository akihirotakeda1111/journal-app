import pytest
from django.utils import timezone

from journal.models import Journal
from journal.models.evidence import Evidence
from journal.serializers.evidence import (
    EvidenceInputSerializer,
    EvidenceOutputSerializer,
)
from datetime import date


def test_evidence_input_serializer_valid():
    """正常にバリデーションが通ること"""

    payload = {
        "key": "evidence/test.pdf",
    }

    serializer = EvidenceInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert validated["key"] == "evidence/test.pdf"


def test_evidence_input_serializer_blank_key():
    """key が空文字の場合はバリデーションエラーになること"""

    payload = {
        "key": "",
    }

    serializer = EvidenceInputSerializer(data=payload)
    assert not serializer.is_valid()
    assert "key" in serializer.errors


def test_evidence_input_serializer_too_long():
    """key が max_length を超える場合はバリデーションエラーになること"""

    payload = {
        "key": "a" * 300,  # 255 を超える
    }

    serializer = EvidenceInputSerializer(data=payload)
    assert not serializer.is_valid()
    assert "key" in serializer.errors


def test_evidence_output_serializer(db):
    """Model -> JSON の変換が正しく行われること"""

    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        recorded_date=date(2026, 1, 1),
    )

    evidence = Evidence.objects.create(
        journal=journal,
        key="evidence/test.pdf",
        uploaded_at=timezone.now(),
    )

    serializer = EvidenceOutputSerializer(evidence)
    data = serializer.data

    assert data["id"] == evidence.id
    assert data["key"] == "evidence/test.pdf"
    assert data["uploaded_at"] == evidence.uploaded_at.isoformat().replace(
        "+00:00", "Z"
    )

    # fields が正しく揃っていること
    assert set(data.keys()) == {"id", "key", "uploaded_at"}
