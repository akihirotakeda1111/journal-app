import pytest
from unittest.mock import patch
from django.db import IntegrityError
from rest_framework import status

from journal.models import Journal, JournalLine
from journal.domain.constants import Side
from journal.services.journal_with_lines import JournalWithLinesService

BASE_CREATE = "/api/journal/"
BASE_CANCEL = "/api/journal/cancel/{journal_id}/"
BASE_REVISE = "/api/journal/revise/{journal_id}/"
BASE_EVIDENCE_LIST = "/api/journal/evidence/list/{journal_id}/"
BASE_TRIAL_BALANCE = "/api/journal/trial_balance/"


def test_create_rolls_back_when_bulk_create_fails(db, setup_accounts):
    """明細作成失敗時、ヘッダー含めロールバックされること"""
    asset, liability, expense, revenue = setup_accounts
    data = {
        "id": "77777777-7777-7777-7777-777777777777",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
        ],
    }

    with patch(
        "journal.services.journal_with_lines.JournalLine.objects.bulk_create",
        side_effect=IntegrityError("forced failure"),
    ):
        with pytest.raises(IntegrityError):
            JournalWithLinesService.create(data)

    assert Journal.objects.count() == 0
    assert JournalLine.objects.count() == 0


def test_revise_rolls_back_when_new_lines_fail(db, setup_accounts):
    """訂正仕訳の明細作成失敗時、逆仕訳・訂正仕訳ともに保存されないこと"""
    asset, liability, expense, revenue = setup_accounts
    original = JournalWithLinesService.create(
        {
            "id": "88888888-8888-8888-8888-888888888888",
            "recorded_date": "2026-01-01",
            "lines": [
                {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
            ],
        }
    )
    new_data = {
        "id": "99999999-9999-9999-9999-999999999999",
        "recorded_date": "2026-01-02",
        "lines": [
            {"account_id": asset.id, "amount": 200, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 200, "side": Side.CREDIT},
        ],
    }

    original_count = Journal.objects.count()
    original_line_count = JournalLine.objects.count()

    call_count = {"n": 0}
    original_bulk_create = JournalLine.objects.bulk_create

    def bulk_create_side_effect(lines):
        call_count["n"] += 1
        if call_count["n"] == 2:
            raise IntegrityError("forced failure on revise lines")
        return original_bulk_create(lines)

    with patch(
        "journal.services.journal_with_lines.JournalLine.objects.bulk_create",
        side_effect=bulk_create_side_effect,
    ):
        with pytest.raises(IntegrityError):
            JournalWithLinesService.revise(original.id, new_data)

    assert Journal.objects.count() == original_count
    assert JournalLine.objects.count() == original_line_count


def test_cancel_not_found_returns_404(client, db):
    """存在しない仕訳の取消で404と標準エラー形式が返ること"""
    journal_id = "99999999-9999-9999-9999-999999999999"
    resp = client.post(BASE_CANCEL.format(journal_id=journal_id), format="json")

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    body = resp.json()
    assert body["error"]["code"] == "JOURNAL_NOT_FOUND"
    assert journal_id in body["error"]["message"]


def test_cancel_already_cancelled_returns_409(client, db, setup_accounts):
    """二重取消で409が返ること"""
    asset, liability, expense, revenue = setup_accounts
    original = JournalWithLinesService.create(
        {
            "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "recorded_date": "2026-01-01",
            "lines": [
                {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
            ],
        }
    )
    JournalWithLinesService.cancel(original.id)

    resp = client.post(
        BASE_CANCEL.format(journal_id=str(original.id)), format="json"
    )

    assert resp.status_code == status.HTTP_409_CONFLICT
    assert resp.json()["error"]["code"] == "CANCEL_ALREADY_EXISTS"


def test_create_duplicate_returns_200_for_idempotency(client, db, setup_accounts):
    """冪等性: 同一IDの再登録は200が返ること"""
    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "recordedDate": "2026-01-01",
        "lines": [
            {"accountId": asset.id, "side": Side.DEBIT, "amount": 100},
            {"accountId": liability.id, "side": Side.CREDIT, "amount": 100},
        ],
    }

    first = client.post(BASE_CREATE, payload, format="json")
    second = client.post(BASE_CREATE, payload, format="json")

    assert first.status_code == status.HTTP_201_CREATED
    assert second.status_code == status.HTTP_200_OK
    assert second.json()["error"]["code"] == "JOURNAL_ALREADY_EXISTS"


def test_revise_not_found_returns_404(client, db, setup_accounts):
    """存在しない仕訳の訂正で404が返ること"""
    asset, liability, expense, revenue = setup_accounts
    payload = {
        "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
        "recordedDate": "2026-01-01",
        "lines": [
            {"accountId": asset.id, "side": Side.DEBIT, "amount": 100},
            {"accountId": liability.id, "side": Side.CREDIT, "amount": 100},
        ],
    }
    resp = client.post(
        BASE_REVISE.format(journal_id="99999999-9999-9999-9999-999999999999"),
        payload,
        format="json",
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["error"]["code"] == "JOURNAL_NOT_FOUND"


def test_view_unhandled_error_returns_generic_500(client):
    """想定外エラーはスタックトレースを返さず500の汎用メッセージになること"""
    with patch(
        "journal.views.journal_with_lines.JournalWithLinesService.list",
        side_effect=RuntimeError("secret internal detail"),
    ):
        resp = client.get("/api/journal/list/")

    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    body = resp.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred."
    assert "secret internal detail" not in str(body)


def test_evidence_list_journal_not_found_returns_404(client, db):
    """存在しない仕訳の証憑一覧で404が返ること"""
    journal_id = "99999999-9999-9999-9999-999999999999"
    resp = client.get(BASE_EVIDENCE_LIST.format(journal_id=journal_id))

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["error"]["code"] == "JOURNAL_NOT_FOUND"


def test_trial_balance_invalid_date_returns_400(client, db):
    """不正な日付形式で400が返ること"""
    resp = client.get(BASE_TRIAL_BALANCE, {"start_date": "2026/01/01"})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["error"]["code"] == "INVALID_DATE_FORMAT"

