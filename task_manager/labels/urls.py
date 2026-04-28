from django.urls import path

from task_manager.labels.views import LabelListView, LabelCreateView

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='index'),
    path('create/', LabelCreateView.as_view(), name='create'),
]
