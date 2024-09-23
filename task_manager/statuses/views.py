from django.views.generic import ListView
from task_manager.mixins import NoLoginMixin
from task_manager.statuses.models import Status


class StatusesListView(NoLoginMixin,
                       ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'
    extra_context = {
        'title': 'Статусы'
    }
