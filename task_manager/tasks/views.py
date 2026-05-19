from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.mixins import LoginRequiredMessagesMixin, UserAccessTestMixin
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMessagesMixin, FilterView):
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter

    def get_queryset(self):
        return (
            Task.objects.select_related('status', 'reporter', 'assignee')
            .only(
                'name',
                'created_at',
                'status__name',
                'reporter__first_name',
                'reporter__last_name',
                'assignee__first_name',
                'assignee__last_name',
            )
            .order_by('created_at')
        )


class TaskDetailView(LoginRequiredMessagesMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'


class TaskCreateView(
    LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView
):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')
    default_status_name = 'Open'

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMessagesMixin, SuccessMessageMixin, UpdateView
):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully updated')


class TaskDeleteView(UserAccessTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully removed')
    permission_url = reverse_lazy('tasks:index')
    permission_message = _('A task can be deleted only by it is author')
