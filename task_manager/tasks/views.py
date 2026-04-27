from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.mixins import LoginRequiredMessagesMixin, UserAccessTestMixin
from task_manager.tasks.models import Status, Task


class TaskListView(LoginRequiredMessagesMixin, ListView):
    template_name = 'tasks/index.html'

    def get_queryset(self):
        return Task.objects.select_related('status', 'reporter', 'assignee').only(
            'name',
            'created_at',
            'status__name',
            'reporter__first_name',
            'reporter__last_name',
            'assignee__first_name',
            'assignee__last_name',
        )


class TaskCreateView(LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = _('Task successfully created')
    default_status_name = 'Open'

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        default_status = Status.objects.filter(name=self.default_status_name).first()

        if default_status:
            initial['status'] = default_status.pk

        return initial


class TaskUpdateView(LoginRequiredMessagesMixin, SuccessMessageMixin, UpdateView):
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
