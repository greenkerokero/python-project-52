from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))

    self_task = BooleanFilter(
        label=_('Only your tasks'),
        widget=forms.CheckboxInput,
        method='filter_self_task',
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels']

    def filter_self_task(self, queryset, name, value):
        if value:
            return queryset.filter(reporter=self.request.user)
        return queryset
