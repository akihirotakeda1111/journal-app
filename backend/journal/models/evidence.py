from django.db import models


class Evidence(models.Model):
    journal = models.ForeignKey(
        "journal.Journal",
        on_delete=models.CASCADE,
        related_name="evidences",
    )

    key = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)
