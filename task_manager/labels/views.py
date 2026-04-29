from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from task_manager.labels.models import Label
from task_manager.labels.mixin import LoginRequiredMessagesMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import LabelForm


class LabelListView(LoginRequiredMessagesMixin, ListView):
    template_name = 'labels/index.html'

    def get_queryset(self):
        return Label.objects.only('id', 'name', 'created_at').order_by('created_at')


class LabelCreateView(LoginRequiredMessagesMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMessagesMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully updated')
