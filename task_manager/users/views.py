from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.users.forms import NewUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/user_create.html'
    form_class = NewUserCreationForm
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')