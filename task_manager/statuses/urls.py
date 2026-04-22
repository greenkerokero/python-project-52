from django.urls import path

from task_manager.statuses.views import StatusListView, StatusCreateView

app_name = 'statuses'

urlpatterns = [
    path('', StatusListView.as_view(), name='index'),
    path('create/', StatusCreateView.as_view(), name='create'),
]
