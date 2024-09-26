from django.urls import path
from task_manager.tasks.views import TasksListView, TaskCreateView

urlpatterns = [
    path('', TasksListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
]