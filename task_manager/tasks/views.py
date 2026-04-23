from django.views.generic import ListView
from task_manager.tasks.models import Task


class TasksListView(ListView):
    template_name = 'tasks/index.html'

    def get_queryset(self):
        return Task.objects.select_related(
            'status', 'reporter', 'assignee'
        ).only(
            'name',
            'created_at',
            'status__name',
            'reporter__first_name',
            'reporter__last_name',
            'assignee__first_name',
            'assignee__last_name',
        )
