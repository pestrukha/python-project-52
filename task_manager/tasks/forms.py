from django import forms
from task_manager.tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Исполнитель',
        widget=forms.Select,
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: obj.get_full_name()