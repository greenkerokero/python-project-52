from django.urls import path

from task_manager.labels.views import LabelListView

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='index'),
]
