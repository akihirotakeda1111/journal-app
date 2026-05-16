from django.db import models
from management.domain.constants import AccountType


class Account(models.Model):

    # 勘定科目ID
    id = models.CharField(max_length=10, primary_key=True)

    # 勘定科目名
    name = models.CharField(max_length=50)

    # 勘定科目種別
    type = models.CharField(max_length=20, choices=AccountType.CHOICES)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} {self.name}"
