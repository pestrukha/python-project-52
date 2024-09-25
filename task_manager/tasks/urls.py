from django.urls import path
from task_manager.tasks.views import TasksListView

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
]