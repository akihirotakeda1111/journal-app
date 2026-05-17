import pytest
from django.core.exceptions import ValidationError
from journal.services.journal_with_lines import JournalWithLinesService
from journal.models import Journal, JournalLine
from journal.domain.constants import AmountRules, JournalType, Side
from journal.exceptions.journal_exceptions import JournalAlreadyExistsError
from uuid import UUID
from datetime import date, datetime, timedelta
from django.utils import timezone


def test_clean_success():
    """正常にデータが正規化されること"""
    id_str = "11111111-1111-1111-1111-111111111111"
    data = {
        "id": id_str,
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": 1, "amount": AmountRules.MIN, "side": Side.DEBIT},
            {"account_id": 2, "amount": AmountRules.MIN, "side": Side.CREDIT},
            {"account_id": 1, "amount": AmountRules.MAX, "side": Side.DEBIT},
            {"account_id": 2, "amount": AmountRules.MAX, "side": Side.CREDIT},
        ],
    }

    cleaned = JournalWithLinesService._clean(data)

    assert isinstance(cleaned["id"], UUID)
    assert cleaned["id"] == UUID(id_str)
    assert isinstance(cleaned["recorded_date"], date)
    assert cleaned["recorded_date"] == date(2026, 1, 1)


def test_clean_missing_id():
    """id がない場合、ValidationErrorが発生すること"""
    data = {
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": 1, "amount": 100, "side": Side.DEBIT},
            {"account_id": 2, "amount": 100, "side": Side.CREDIT},
        ],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_clean_missing_recorded_date():
    """recorded_date がない場合、ValidationErrorが発生すること"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "lines": [
            {"account_id": 1, "amount": 100, "side": Side.DEBIT},
            {"account_id": 2, "amount": 100, "side": Side.CREDIT},
        ],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_clean_empty_lines():
    """lines が空の場合、ValidationErrorが発生すること"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_clean_missing_account_id():
    """account_id がない場合、ValidationErrorが発生すること"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": 1, "amount": 100, "side": Side.DEBIT},
            {"amount": 100, "side": Side.CREDIT},
        ],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_clean_missing_amount():
    """amount がない場合、ValidationErrorが発生すること"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": 1, "amount": 100, "side": Side.DEBIT},
            {"account_id": 2, "side": Side.CREDIT},
        ],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_clean_invalid_side():
    """side が無効な値の場合、ValidationErrorが発生すること"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": 1, "amount": 100, "side": Side.CREDIT},
            {"account_id": 2, "amount": 100, "side": "INVALID"},
        ],
    }
    with pytest.raises(ValidationError):
        JournalWithLinesService._clean(data)


def test_create_success(db, setup_accounts):
    """仕訳ヘッダーと仕訳明細が正常に作成される"""

    asset, liability, expense, revenue = setup_accounts
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "description": "テスト仕訳",
        "lines": [
            {"account_id": asset.id, "amount": 1000, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 1000, "side": Side.CREDIT},
        ],
    }
    journal = JournalWithLinesService.create(data)
    lines = list(journal.lines.all())

    # 1件の仕訳と2件の仕訳明細が保存されていること
    assert Journal.objects.count() == 1
    assert JournalLine.objects.count() == 2

    # 仕訳が正しく保存されていること
    assert journal.id == Journal.to_uuid(data["id"])
    assert journal.recorded_date == Journal.to_date(data["recorded_date"])
    assert journal.description == data["description"]
    assert journal.type == JournalType.NORMAL
    assert journal.original_journal is None

    # 仕訳明細が正しく保存されていること
    assert lines[0].account_id == asset.id
    assert lines[0].amount == 1000
    assert lines[1].account_id == liability.id
    assert lines[1].amount == -1000


def test_create_clean_validation(db):
    """仕訳入力データの検証に失敗した場合、ValidationErrorが発生する"""
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "recorded_date": "2026-01-01",
        "lines": [],
    }

    with pytest.raises(ValidationError):
        JournalWithLinesService.create(data)


def test_create_duplicate_id(db, setup_accounts):
    """ID重複の場合、JournalAlreadyExistsErrorが発生する"""

    asset, liability, expense, revenue = setup_accounts
    data = {
        "id": "22222222-2222-2222-2222-222222222222",
        "recorded_date": "2026-01-01",
        "lines": [
            {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
        ],
    }

    # 1回目：成功
    JournalWithLinesService.create(data)

    # 2回目：エラー
    with pytest.raises(JournalAlreadyExistsError):
        JournalWithLinesService.create(data)


def test_cancel_success(db, setup_accounts):
    """逆仕訳が正しく生成される"""

    asset, liability, expense, revenue = setup_accounts

    # 元仕訳の作成
    original = JournalWithLinesService.create(
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "recorded_date": "2026-01-01",
            "description": "元仕訳",
            "lines": [
                {"account_id": asset.id, "amount": 500, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 500, "side": Side.CREDIT},
            ],
        }
    )
    original_lines = list(JournalLine.objects.filter(journal=original))

    cancel_journal = JournalWithLinesService.cancel(original.id)
    cancel_journal_lines = list(JournalLine.objects.filter(journal=cancel_journal))
    cancel = Journal.objects.get(type=JournalType.CANCEL)
    cancel_lines = list(JournalLine.objects.filter(journal=cancel))

    # 元仕訳、逆仕訳の2つが存在すること
    assert Journal.objects.count() == 2

    # 元仕訳と逆仕訳の明細行数が同じであること
    assert len(original_lines) == len(cancel_lines)

    # 逆仕訳が正しく保存されていること
    assert cancel.type == JournalType.CANCEL
    assert cancel.recorded_date == original.recorded_date
    assert cancel.description == f"【取消】 {original.description}"

    # 逆仕訳が元仕訳と紐づいていること
    assert cancel.original_journal_id == original.id

    # 元仕訳の明細と同じ勘定科目の逆仕訳の明細が存在すること
    for original_line in original_lines:
        cancel_line = next(
            l for l in cancel_lines if l.account_id == original_line.account_id
        )

        # 金額が反転していること
        assert cancel_line.amount == -original_line.amount


def test_revise_success(db, setup_accounts):
    """逆仕訳と訂正仕訳が正しく生成される"""

    asset, liability, expense, revenue = setup_accounts

    # 元仕訳の作成
    original = JournalWithLinesService.create(
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "recorded_date": "2026-01-01",
            "description": "元仕訳",
            "lines": [
                {"account_id": asset.id, "amount": 500, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 500, "side": Side.CREDIT},
            ],
        }
    )
    original_lines = list(JournalLine.objects.filter(journal=original))

    # 訂正仕訳の作成
    new_data = {
        "id": "44444444-4444-4444-4444-444444444444",
        "recorded_date": "2026-01-02",
        "description": "訂正仕訳",
        "lines": [
            {"account_id": asset.id, "amount": 300, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 300, "side": Side.CREDIT},
        ],
    }
    new_journal = JournalWithLinesService.revise(original.id, new_data)
    new_journal_lines = list(JournalLine.objects.filter(journal=new_journal))
    cancel = Journal.objects.get(type=JournalType.CANCEL)
    cancel_lines = list(JournalLine.objects.filter(journal=cancel))

    # 元仕訳、逆仕訳、訂正仕訳の3つが存在すること
    assert Journal.objects.count() == 3

    # 元仕訳と逆仕訳の明細行数が同じであること
    assert len(original_lines) == len(cancel_lines)

    # 逆仕訳が正しく保存されていること
    assert cancel.type == JournalType.CANCEL
    assert cancel.recorded_date == original.recorded_date
    assert cancel.description == f"【取消】 {original.description}"

    # 逆仕訳が元仕訳と紐づいていること
    assert cancel.original_journal_id == original.id

    # 元仕訳の明細と同じ勘定科目の逆仕訳の明細が存在すること
    for original_line in original_lines:
        cancel_line = next(
            l for l in cancel_lines if l.account_id == original_line.account_id
        )

        # 金額が反転していること
        assert cancel_line.amount == -original_line.amount

    # 訂正仕訳明細が2件存在すること
    assert len(new_journal_lines) == 2

    # 訂正仕訳が正しく保存されていること
    assert new_journal.type == JournalType.NORMAL
    assert new_journal.recorded_date == new_data["recorded_date"]
    assert new_journal.description == new_data["description"]

    # 訂正仕訳明細が正しく保存されていること
    debit_line = next(l for l in new_journal_lines if l.account_id == asset.id)
    assert debit_line.amount == 300

    credit_line = next(l for l in new_journal_lines if l.account_id == liability.id)
    assert credit_line.amount == -300

    # 訂正仕訳が逆仕訳と紐づいていること
    assert new_journal.original_journal_id == cancel.id


def test_revise_clean_validation(db, setup_accounts):
    """訂正仕訳入力データの検証に失敗した場合、ValidationErrorが発生する"""

    asset, liability, expense, revenue = setup_accounts

    original = JournalWithLinesService.create(
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "recorded_date": "2026-01-01",
            "lines": [{"account_id": asset.id, "amount": 100, "side": Side.DEBIT}],
        }
    )
    new_data = {
        "id": "22222222-2222-2222-2222-222222222222",
        "recorded_date": "2026-01-01",
        "lines": [],
    }

    with pytest.raises(ValidationError):
        JournalWithLinesService.revise(original.id, new_data)


def test_revise_not_found(db):
    """存在しないIDが指定された場合、ValidationError"""
    with pytest.raises(ValidationError):
        JournalWithLinesService.revise("99999999-9999-9999-9999-999999999999", {})


def test_revise_double_revise(db, setup_accounts):
    """訂正済みの仕訳を再度訂正した場合、ValidationError"""

    asset, liability, expense, revenue = setup_accounts

    original = JournalWithLinesService.create(
        {
            "id": "55555555-5555-5555-5555-555555555555",
            "recorded_date": "2026-01-01",
            "lines": [
                {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
            ],
        }
    )

    new_data = {
        "id": "66666666-6666-6666-6666-666666666666",
        "recorded_date": "2026-01-02",
        "lines": [
            {"account_id": asset.id, "amount": 200, "side": Side.DEBIT},
            {"account_id": liability.id, "amount": 200, "side": Side.CREDIT},
        ],
    }

    # 1回目：成功
    JournalWithLinesService.revise(original.id, new_data)

    # 2回目：エラー
    with pytest.raises(ValidationError):
        JournalWithLinesService.revise(original.id, new_data)


def test_list(db, setup_accounts):
    """
    最新のデータから取得されること（recorded_date 降順、同日なら created_at 降順）。
    構成:
      - same_date_old: recorded_date=2026-01-03, created_at = base +1h
      - same_date_early: recorded_date=2026-01-03, created_at = base
      - later_date: recorded_date=2026-01-04, created_at = base +23h
    期待順: later_date, same_date_old, same_date_early
    """

    asset, liability, expense, revenue = setup_accounts

    base = timezone.make_aware(datetime(2026, 1, 3, 9, 0, 0))

    same_date_old = JournalWithLinesService.create(
        {
            "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "recorded_date": "2026-01-03",
            "description": "old_same_day",
            "lines": [
                {"account_id": asset.id, "amount": 100, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 100, "side": Side.CREDIT},
            ],
        }
    )

    same_date_early = JournalWithLinesService.create(
        {
            "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "recorded_date": "2026-01-03",
            "description": "early_same_day",
            "lines": [
                {"account_id": asset.id, "amount": 200, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 200, "side": Side.CREDIT},
            ],
        }
    )

    later_date = JournalWithLinesService.create(
        {
            "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "recorded_date": "2026-01-04",
            "description": "later_date",
            "lines": [
                {"account_id": asset.id, "amount": 300, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 300, "side": Side.CREDIT},
            ],
        }
    )

    # created_at を明示的に設定
    Journal.objects.filter(id=same_date_old.id).update(
        created_at=base + timedelta(hours=1)
    )
    Journal.objects.filter(id=same_date_early.id).update(created_at=base)
    Journal.objects.filter(id=later_date.id).update(
        created_at=base + timedelta(hours=23)
    )

    results = list(JournalWithLinesService.list())

    assert len(results) >= 3
    assert results[0].id == later_date.id
    assert results[1].id == same_date_old.id
    assert results[2].id == same_date_early.id


def test_history(db, setup_accounts):
    """original_journal_id を辿り、最古の仕訳から順に履歴が取得されること。"""

    asset, liability, expense, revenue = setup_accounts

    # 元仕訳 first
    first = JournalWithLinesService.create(
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "recorded_date": "2026-01-01",
            "description": "first",
            "lines": [
                {"account_id": asset.id, "amount": 500, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 500, "side": Side.CREDIT},
            ],
        }
    )

    # first を訂正 -> cancel1 + new1
    new1 = JournalWithLinesService.revise(
        first.id,
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "recorded_date": "2026-01-02",
            "description": "new1",
            "lines": [
                {"account_id": asset.id, "amount": 400, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 400, "side": Side.CREDIT},
            ],
        },
    )

    # new1 を訂正 -> cancel2 + new2
    new2 = JournalWithLinesService.revise(
        new1.id,
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "recorded_date": "2026-01-03",
            "description": "new2",
            "lines": [
                {"account_id": asset.id, "amount": 300, "side": Side.DEBIT},
                {"account_id": liability.id, "amount": 300, "side": Side.CREDIT},
            ],
        },
    )

    # cancel レコードを original_journal から取得
    cancel1 = Journal.objects.get(original_journal_id=first.id)
    cancel2 = Journal.objects.get(original_journal_id=new1.id)

    # created_at をシャッフル
    base = timezone.make_aware(datetime(2026, 1, 1, 9, 0, 0))
    Journal.objects.filter(id=first.id).update(created_at=base + timedelta(hours=2))
    Journal.objects.filter(id=cancel1.id).update(created_at=base + timedelta(hours=1))
    Journal.objects.filter(id=new1.id).update(created_at=base + timedelta(hours=4))
    Journal.objects.filter(id=cancel2.id).update(created_at=base + timedelta(hours=3))
    Journal.objects.filter(id=new2.id).update(created_at=base + timedelta(hours=5))

    # 最新データ(new2)から history を取得
    history = JournalWithLinesService.history(new2.id)

    # 期待順（first, cancel1, new1, cancel2, new2）
    expected_ids = [first.id, cancel1.id, new1.id, cancel2.id, new2.id]
    assert [j.id for j in history] == expected_ids

    # 先頭が最も古い（元仕訳 first）、末尾が最新（new2）
    assert history[0].id == first.id
    assert history[-1].id == new2.id
