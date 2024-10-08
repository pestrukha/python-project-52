from task_manager.mixins import AuthRequiredMixin
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
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = 'tasks/task_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskView(AuthRequiredMixin, DetailView):
    template_name = 'tasks/one_task.html'
    model = Task
    context_object_name = 'task'


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/task_update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    success_message = _('Task successfully changed')


class TaskDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tasks/task_delete.html'
    model = Task
    success_url = reverse_lazy('task_list')
    success_message = _('Task successfully delete')

    def check_task_author(self):
        if self.get_object().author != self.request.user:
            messages.error(
                self.request,
                _('The task can be deleted only by its author'))
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
