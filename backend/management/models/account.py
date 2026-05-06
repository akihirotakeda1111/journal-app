from django.db import models


class Account(models.Model):
    class TypeChoices(models.TextChoices):
        ASSET = "ASSET", "資産"
        LIABILITY = "LIABILITY", "負債"
        EQUITY = "EQUITY", "純資産"
        REVENUE = "REVENUE", "収益"
        EXPENSE = "EXPENSE", "費用"

    # 勘定科目ID
    id = models.CharField(max_length=10, primary_key=True)

    # 勘定科目名
    name = models.CharField(max_length=50)

    # 勘定科目種別
    type = models.CharField(max_length=20, choices=TypeChoices.choices)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} {self.name}"
