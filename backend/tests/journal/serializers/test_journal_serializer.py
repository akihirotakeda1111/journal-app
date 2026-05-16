import pytest
from journal.models import Journal
from journal.serializers.journal import JournalInputSerializer, JournalOutputSerializer
from journal.domain.constants import JournalType
from datetime import date


def test_journal_input_serializer_valid():
    """正常にバリデーションが通ること"""

    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        # description: None
    }

    serializer = JournalInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    # id -> UUID, recorded_date -> date
    assert hasattr(validated["id"], "hex")
    assert validated["recorded_date"] == date(2026, 1, 1)
    # description -> None
    assert "description" not in validated


def test_journal_input_serializer_blank_description():
    """description が空文字でも許容されること"""

    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "description": "",
    }

    serializer = JournalInputSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    # description -> blank
    assert validated.get("description", None) == ""


def test_journal_input_serializer_invalid():
    """不正な UUID / 日付フォーマットはバリデーションエラーになること"""

    invalid_uuid_payload = {
        "id": "not-a-uuid",
        "recorded_date": "2026-01-01",
    }
    serializer1 = JournalInputSerializer(data=invalid_uuid_payload)
    assert not serializer1.is_valid()
    assert "id" in serializer1.errors

    invalid_date_payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-13-01",
    }
    serializer2 = JournalInputSerializer(data=invalid_date_payload)
    assert not serializer2.is_valid()
    assert "recorded_date" in serializer2.errors


def test_journal_output_serializer(db):
    """Moldel -> JSON の変換が正しく行われること"""

    journal = Journal.objects.create(
        id="11111111-1111-1111-1111-111111111111",
        recorded_date=date(2026, 1, 1),
        description="Test",
        type=JournalType.NORMAL,
    )

    serializer = JournalOutputSerializer(journal)
    data = serializer.data
    assert data["id"] == str(journal.id)
    assert data["recorded_date"] == "2026-01-01"
    assert data["description"] == "Test"
    assert data["type"] == JournalType.NORMAL
    assert set(data.keys()) == {"id", "recorded_date", "description", "type"}
