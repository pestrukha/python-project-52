from django.urls import path
from task_manager.tasks.views import TasksListView, TaskCreateView, TaskView

urlpatterns = [
    path('', TasksListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskView.as_view(), name='one_task'),
]