from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import AuthRequiredMixin
from task_manager.labels.models import Label
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


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


class LabelDeleteView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_message = 'Метка успешно удалена'
    success_url = reverse_lazy('label_list')
    protected_message = 'Невозможно удалить метку, потому что она используется'
    protected_url = 'label_list'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
