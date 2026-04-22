from django.views.generic import ListView
from task_manager.statuses.models import Status


class StatusListView(ListView):
    template_name = 'statuses/index.html'

    def get_queryset(self):
        return Status.objects.only('name')
