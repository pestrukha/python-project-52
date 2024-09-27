from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.LabelListView.as_view(), name='label_list'),
    path('create/', views.LabelCreateView.as_view(), name='label_create'),
]