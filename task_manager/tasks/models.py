from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150, verbose_name=_('Name'), unique=True
    )
    description = models.TextField(
        max_length=300, verbose_name=_('Description')
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name='status', verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author', verbose_name=_('Only your own tasks')
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='executor', verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label, through='TaskLabelDependence', through_fields=('task', 'label'), blank=True,
        related_name='labels', verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Creation date')
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['id']

    def __str__(self):
        return self.name


class TaskLabelDependence(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
