from django.db import models
from datetime import datetime, date
from uuid import UUID


class Journal(models.Model):
    # PK
    id = models.UUIDField(primary_key=True, editable=False)

    # 計上日
    recorded_date = models.DateField()

    # 摘要
    description = models.TextField(null=True, blank=True)

    # 状態
    type = models.CharField(
        max_length=10,
        choices=(
            ("NORMAL", "通常"),
            ("CANCEL", "取消"),
        ),
        default="NORMAL",
    )

    # 元仕訳
    original_journal = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="child",
    )

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def to_uuid(value):
        return UUID(value) if isinstance(value, str) else value

    @staticmethod
    def to_date(value):
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%Y-%m-%d").date()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(type__in=["NORMAL", "CANCEL"]),
                name="chk_journals_type",
            )
        ]
