from django import forms
from django_filters import BooleanFilter, FilterSet
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    own_tasks = BooleanFilter(
        field_name='author',
        method='filtered_own_tasks',
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def filtered_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user.pk
            return queryset.filter(author=user)
        return queryset