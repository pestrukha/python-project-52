from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Имя', unique=True
    )
    description = models.TextField(
        max_length=300, verbose_name='Описание'
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='status', verbose_name='Статус'
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author', verbose_name='Только свои задачи'
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='executor', verbose_name='Исполнитель'
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
