from django.db import models


class SyncExecution(models.Model):
    DIRECTION_BITRIX_TO_ONEC = "bitrix_to_1c"
    DIRECTION_ONEC_TO_BITRIX = "1c_to_bitrix"
    DIRECTION_BOTH = "both"

    DIRECTION_CHOICES = [
        (DIRECTION_BITRIX_TO_ONEC, "Bitrix -> 1C"),
        (DIRECTION_ONEC_TO_BITRIX, "1C -> Bitrix"),
        (DIRECTION_BOTH, "В обе стороны"),
    ]

    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "В процессе"),
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Ошибка"),
    ]

    direction = models.CharField(max_length=32, choices=DIRECTION_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    pulled_count = models.PositiveIntegerField(default=0)
    pushed_count = models.PositiveIntegerField(default=0)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self) -> str:
        return f"{self.direction} ({self.status})"
