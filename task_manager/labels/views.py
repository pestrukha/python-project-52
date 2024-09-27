from django.views.generic import ListView, CreateView, UpdateView
from task_manager.mixins import AuthRequiredMixin
from task_manager.labels.models import Label
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/label_list.html'


class LabelCreateView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно создана'


class LabelEditView(SuccessMessageMixin,
                    AuthRequiredMixin,
                    UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно изменена'
