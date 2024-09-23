from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusesListView.as_view(), name='statuses_list'),
]