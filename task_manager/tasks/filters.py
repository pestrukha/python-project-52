from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    own_tasks = BooleanFilter(
        field_name='author',
        method='filtered_own_tasks',
        widget=forms.CheckboxInput,
    )

    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label='Метка',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filtered_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user.pk
            return queryset.filter(author=user)
        return queryset
