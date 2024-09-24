from django.views.generic import ListView, CreateView
from task_manager.mixins import NoLoginMixin
from task_manager.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.statuses.forms import StatusForm


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
    success_url = reverse_lazy('statuses_list')
    extra_context = {
        'title': 'Создать статус',
        'button_text': 'Создать',
    }
