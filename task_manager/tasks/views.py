from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import LoginRequiredMessagesMixin
from task_manager.tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


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


class TasksCreateView(LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
