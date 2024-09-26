from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class NoLoginMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход')
        return redirect(reverse_lazy('login'))


class AuthorMixin(UserPassesTestMixin):
    author_permission_message = ''
    author_permission_url = ''

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_permission_message)
        return redirect(self.author_permission_url)
