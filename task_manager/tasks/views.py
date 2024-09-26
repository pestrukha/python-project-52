from task_manager.mixins import NoLoginMixin
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from task_manager.tasks.forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect


User = get_user_model()


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


class TasksListView(NoLoginMixin, FilterView):
    template_name = 'tasks/task_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskView(NoLoginMixin, DetailView):
    template_name = 'tasks/one_task.html'
    model = Task
    context_object_name = 'task'


class TaskUpdateView(NoLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/task_update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(NoLoginMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
    model = Task
    success_url = reverse_lazy('task_list')
    success_message = 'Задача успешно удалена'

    def check_task_author(self):
        if self.get_object().author != self.request.user:
            messages.error(
                self.request,
                'Задачу может удалить только её автор')
            return False
        return True

    def get(self, request, *args, **kwargs):
        if not self.check_task_author():
            return redirect('task_list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.check_task_author():
            return redirect('task_list')
        return super().post(request, *args, **kwargs)
