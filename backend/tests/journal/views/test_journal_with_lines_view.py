import pytest
from unittest.mock import patch
from rest_framework import status
from uuid import UUID
from journal.domain.constants import Side, JournalType
from management.domain.constants import AccountType

BASE_CREATE = "/api/journal/"
BASE_CANCEL = "/api/journal/cancel/{journal_id}/"
BASE_REVISE = "/api/journal/revise/{journal_id}/"
BASE_LIST = "/api/journal/list/"
BASE_HISTORY = "/api/journal/{journal_id}/history/"


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


def test_journal_with_lines_view_create(client):
    """仕訳登録リクエストが正常に処理され、レスポンスが返ること"""

    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": "T01", "side": Side.DEBIT, "amount": 100},
            {"account_id": "T02", "side": Side.CREDIT, "amount": 100},
        ],
    }

    fake_journal = {
        "id": payload["id"],
        "recordedDate": payload["recorded_date"],
        "lines": [
            {"accountId": "T01", "side": Side.DEBIT, "amount": 100},
            {"accountId": "T02", "side": Side.CREDIT, "amount": 100},
        ],
    }

    input_path = "journal.views.journal_with_lines.JournalWithLinesInputSerializer"
    output_path = "journal.views.journal_with_lines.JournalWithLinesOutputSerializer"
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.create"

    with patch(input_path, new=DummyInputSerializer), patch(
        output_path, new=DummyOutputSerializer
    ), patch(service_path, return_value=fake_journal) as mock_create:
        resp = client.post(BASE_CREATE, payload, format="json")

    mock_create.assert_called_once_with(payload)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json() == fake_journal


def test_journal_with_lines_view_cancel(client):
    """逆訂正リクエストが正常に処理され、レスポンスが返ること"""

    journal_id_str = "11111111-1111-1111-1111-111111111111"
    journal_id_uuid = UUID(journal_id_str)

    fake_journal = {
        "id": journal_id_str,
        "recordedDate": "2026-01-01",
        "description": "【取消】元仕訳",
        "type": JournalType.CANCEL,
        "lines": [
            {"accountId": "T01", "side": Side.CREDIT, "amount": 200},
            {"accountId": "T03", "side": Side.DEBIT, "amount": 200},
        ],
    }

    output_path = "journal.views.journal_with_lines.JournalWithLinesOutputSerializer"
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.cancel"

    with patch(output_path, new=DummyOutputSerializer), patch(
        service_path, return_value=fake_journal
    ) as mock_cancel:
        resp = client.post(BASE_CANCEL.format(journal_id=journal_id_str), format="json")

    mock_cancel.assert_called_once_with(journal_id_uuid)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json() == fake_journal


def test_journal_with_lines_view_revise(client):
    """仕訳訂正リクエストが正常に処理され、レスポンスが返ること"""

    journal_id_str = "11111111-1111-1111-1111-111111111111"
    journal_id_uuid = UUID(journal_id_str)

    payload = {
        "recorded_date": "2026-01-02",
        "lines": [
            {"account_id": "T01", "side": Side.DEBIT, "amount": 200},
            {"account_id": "T03", "side": Side.CREDIT, "amount": 200},
        ],
    }

    fake_journal = {
        "id": journal_id_str,
        "recordedDate": payload["recorded_date"],
        "lines": [
            {"accountId": "T01", "side": Side.DEBIT, "amount": 200},
            {"accountId": "T03", "side": Side.CREDIT, "amount": 200},
        ],
    }

    input_path = "journal.views.journal_with_lines.JournalWithLinesInputSerializer"
    output_path = "journal.views.journal_with_lines.JournalWithLinesOutputSerializer"
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.revise"

    with patch(input_path, new=DummyInputSerializer), patch(
        output_path, new=DummyOutputSerializer
    ), patch(service_path, return_value=fake_journal) as mock_revise:
        resp = client.post(
            BASE_REVISE.format(journal_id=journal_id_str), payload, format="json"
        )

    mock_revise.assert_called_once_with(journal_id_uuid, payload)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json() == fake_journal


def test_journal_with_lines_view_list(client):
    """一覧取得リクエストが正常に処理され、レスポンスが返ること"""

    fake_list = [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "recordedDate": "2026-01-01",
            "lines": [],
        },
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "recordedDate": "2026-01-02",
            "lines": [],
        },
    ]

    output_path = "journal.views.journal_with_lines.JournalWithLinesOutputSerializer"
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.list"

    with patch(output_path, new=DummyOutputSerializer), patch(
        service_path, return_value=fake_list
    ) as mock_list:
        resp = client.get(BASE_LIST)

    mock_list.assert_called_once()
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_list


def test_journal_with_lines_view_history(client):
    """履歴取得リクエストが正常に処理され、レスポンスが返ること"""

    journal_id_str = "11111111-1111-1111-1111-111111111111"
    journal_id_uuid = UUID(journal_id_str)

    fake_history = [
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "recordedDate": "2026-01-01",
            "description": "テスト仕訳",
            "type": JournalType.NORMAL,
            "lines": [
                {
                    "accountId": "101",
                    "side": Side.DEBIT,
                    "amount": 1000,
                    "account": {
                        "id": "101",
                        "name": AccountType.LABELS[AccountType.ASSET],
                        "type": AccountType.ASSET,
                    },
                }
            ],
        },
    ]

    output_path = (
        "journal.views.journal_with_lines.JournalWithLinesAndAccountSerializer"
    )
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.history"

    with patch(output_path, new=DummyOutputSerializer), patch(
        service_path, return_value=fake_history
    ) as mock_history:
        resp = client.get(BASE_HISTORY.format(journal_id=journal_id_str))

    mock_history.assert_called_once_with(journal_id_uuid)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_history


def test_journal_with_lines_view_list_unhandled_error_returns_500(client):
    """想定外エラーは500の汎用メッセージになること"""
    service_path = "journal.views.journal_with_lines.JournalWithLinesService.list"

    with patch(service_path, side_effect=RuntimeError("secret internal detail")):
        resp = client.get(BASE_LIST)

    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    body = resp.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred."
    assert "secret internal detail" not in str(body)
