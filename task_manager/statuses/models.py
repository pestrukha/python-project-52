from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=150, unique=True, blank=False, verbose_name="Name"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Creation date"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
