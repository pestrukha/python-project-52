from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import NoLoginMixin
from task_manager.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.statuses.forms import StatusForm
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect


class StatusesListView(NoLoginMixin,
                       ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'
    extra_context = {
        'title': 'Статусы'
    }


class StatusCreateView(NoLoginMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_message = 'Статус успешно создан'
    success_url = reverse_lazy('status_list')
    extra_context = {
        'title': 'Создать статус',
        'button_text': 'Создать',
    }


class StatusUpdateView(NoLoginMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_message = 'Статус успешно изменён'
    success_url = reverse_lazy('status_list')
    extra_context = {
        'title': 'Изменить статус',
        'button_text': 'Изменить',
    }


class StatusDeleteView(NoLoginMixin,
                       SuccessMessageMixin,
                       DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_message = 'Статус успешно удалён'
    success_url = reverse_lazy('status_list')
    protected_message = 'Невозможно удалить статус, потому что он используется'
    protected_url = reverse_lazy('status_list')
    extra_context = {
        'title': 'Удалить статус',
        'button_text': 'Удалить',
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
