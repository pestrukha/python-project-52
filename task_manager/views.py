from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/user_login.html'
    next_page = reverse_lazy('index')
    success_message = 'Вы залогинены'


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
