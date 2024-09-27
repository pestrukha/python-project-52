from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.users.forms import NewUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import AuthRequiredMixin


User = get_user_model()


class AuthenticationMixin(AuthRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            messages.error(
                self.request, 'У вас нет прав для изменения другого пользователя')
            return redirect('user_list')


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/user_create.html'
    form_class = NewUserCreationForm
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(AuthenticationMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = NewUserCreationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Информация о пользователе изменена'


class UserDeleteView(AuthenticationMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Пользователь удалён'
