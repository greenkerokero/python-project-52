from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import LoginRequiredMessagesMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMessagesMixin, ListView):
    template_name = 'statuses/index.html'

    def get_queryset(self):
        return Status.objects.only('id', 'name', 'created_at').order_by(
            'created_at'
        )


class StatusCreateView(
    LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully created')


class StatusUpdateView(
    LoginRequiredMessagesMixin, SuccessMessageMixin, UpdateView
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully updated')


class StatusDeleteView(
    LoginRequiredMessagesMixin, SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Status successfully removed')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _('Cannot delete status'))
            return redirect(self.success_url)
