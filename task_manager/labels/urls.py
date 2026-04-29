from django.urls import path

from task_manager.labels.views import LabelListView, LabelCreateView, LabelUpdateView

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='index'),
    path('create/', LabelCreateView.as_view(), name='create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='update'),
]
