from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import AuthRequiredMixin
from task_manager.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from task_manager.statuses.forms import StatusForm
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class StatusesListView(AuthRequiredMixin,
                       ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(AuthRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_message = _('Status successfully created')
    success_url = reverse_lazy('status_list')


class StatusUpdateView(AuthRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('status_list')


class StatusDeleteView(AuthRequiredMixin,
                       SuccessMessageMixin,
                       DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_message = _('Status successfully deleted')
    success_url = reverse_lazy('status_list')
    protected_message = _(
        'It is not possible to delete the status, it is in use'
    )
    protected_url = reverse_lazy('status_list')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
