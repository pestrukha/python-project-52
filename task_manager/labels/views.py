from django.views.generic import ListView
from task_manager.mixins import NoLoginMixin
from task_manager.labels.models import Label


class LabelListView(NoLoginMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/label_list.html'
