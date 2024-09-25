from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Name', unique=True
    )
    description = models.TextField(
        max_length=300, verbose_name='Description'
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='status', verbose_name='Status'
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author', verbose_name='Author'
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='executor', verbose_name='Executor'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date'
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['id']

    def __str__(self):
        return self.name
