from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import ProtectedError


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(reverse_lazy('login'))


class DeleteProtectionMixin:
    rejection_message = ''
    rejection_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.rejection_message)
            return redirect(self.rejection_url)
