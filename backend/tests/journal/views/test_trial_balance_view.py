import pytest
from unittest.mock import patch
from rest_framework import status

BASE_URL = "/api/journal/trial_balance/"


def test_trial_balance_view_get_with_param(client):
    """パラメータを含めたリクエストが正常に処理され、レスポンスが返ること"""

    start = "2026-01-01"
    end = "2026-01-31"
    fake_result = [{"accountId": "T01", "balance": 100}]

    with patch(
        "journal.views.trial_balance.TrialBalanceService.get", return_value=fake_result
    ) as mock_get:
        resp = client.get(BASE_URL, {"start_date": start, "end_date": end})

    mock_get.assert_called_once_with(start, end)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_result


def test_trial_balance_view_get_none_param(client):
    """パラメータのないリクエストが正常に処理され、レスポンスが返ること"""

    fake_result = [{"accountId": "T01", "balance": 0}]

    with patch(
        "journal.views.trial_balance.TrialBalanceService.get", return_value=fake_result
    ) as mock_get:
        resp = client.get(BASE_URL)

    mock_get.assert_called_once_with(None, None)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == fake_result


def test_trial_balance_view_unhandled_error_returns_500(client):
    """想定外エラーは500の汎用メッセージになること"""
    with patch(
        "journal.views.trial_balance.TrialBalanceService.get",
        side_effect=RuntimeError("secret internal detail"),
    ) as mock_get:
        resp = client.get(
            BASE_URL, {"start_date": "2026-01-01", "end_date": "2026-01-31"}
        )

    mock_get.assert_called_once()
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    body = resp.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred."
    assert "secret internal detail" not in str(body)
