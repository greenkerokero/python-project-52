from django.views.generic import ListView
from task_manager.labels.models import Label
from task_manager.labels.mixin import LoginRequiredMessagesMixin


class LabelListView(LoginRequiredMessagesMixin, ListView):
    template_name = 'labels/index.html'

    def get_queryset(self):
        return Label.objects.only('id', 'name', 'created_at').order_by('created_at')
