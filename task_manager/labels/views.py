from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import AuthRequiredMixin
from task_manager.labels.models import Label
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


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
    success_message = _('Label successfully created')


class LabelEditView(SuccessMessageMixin,
                    AuthRequiredMixin,
                    UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label successfully changed')


class LabelDeleteView(AuthRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_message = _('Label successfully delete')
    success_url = reverse_lazy('label_list')
    protected_message = _(
        'It is not possible to delete the label, it is in use')
    protected_url = 'label_list'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
