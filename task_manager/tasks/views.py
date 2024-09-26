from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import NoLoginMixin
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from task_manager.tasks.forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


User = get_user_model()


class TasksListView(NoLoginMixin, FilterView):
    template_name = 'tasks/task_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskCreateView(NoLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)
