from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView

from task_manager.statuses.forms import StatusCreateForm
from task_manager.statuses.mixins import LoginRequiredMessagesMixin
from task_manager.statuses.models import Status


class StatusListView(ListView):
    template_name = 'statuses/index.html'

    def get_queryset(self):
        return Status.objects.only('id', 'name', 'created_at')


class StatusCreateView(LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully created')
