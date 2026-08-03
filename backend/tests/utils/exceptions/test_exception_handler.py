import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.exceptions.application_errors import (
    ApplicationValidationError,
    ConflictError,
    RecordNotFoundError,
)
from utils.exceptions.exception_handler import custom_exception_handler


class _StubView(APIView):
    pass


def _handle(exc):
    request = APIRequestFactory().get("/")
    return custom_exception_handler(exc, {"view": _StubView(), "request": request})


def test_handler_maps_validation_error_to_400():
    response = _handle(ApplicationValidationError("id is required"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "error": {"code": "VALIDATION_ERROR", "message": "id is required"}
    }


def test_handler_maps_record_not_found_to_404():
    exc = RecordNotFoundError("Resource missing", code="JOURNAL_NOT_FOUND")
    response = _handle(exc)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"]["code"] == "JOURNAL_NOT_FOUND"


def test_handler_maps_conflict_to_409():
    exc = ConflictError("Already exists", code="CANCEL_ALREADY_EXISTS")
    response = _handle(exc)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.data["error"]["code"] == "CANCEL_ALREADY_EXISTS"


def test_handler_idempotency_override_returns_200():
    from journal.exceptions.journal_exceptions import JournalAlreadyExistsError

    response = _handle(JournalAlreadyExistsError("11111111-1111-1111-1111-111111111111"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["error"]["code"] == "JOURNAL_ALREADY_EXISTS"


def test_handler_unhandled_exception_returns_generic_500():
    response = _handle(RuntimeError("boom"))

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data == {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
        }
    }
    assert "boom" not in str(response.data)
