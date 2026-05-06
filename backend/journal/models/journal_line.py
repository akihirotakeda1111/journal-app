from django.db import models
from management.models import Account


class JournalLine(models.Model):
    # PK
    id = models.BigAutoField(primary_key=True)

    # 仕訳ヘッダー
    journal = models.ForeignKey(
        "Journal",
        on_delete=models.CASCADE,  # 親が消えたら明細も消える
        related_name="lines",
        db_index=True,
    )

    # 勘定科目
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="journal_lines"
    )

    # 金額
    amount = models.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(amount=0),
                name="chk_amount_not_zero",
            ),
        ]
