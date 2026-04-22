from django.urls import path

from task_manager.statuses.views import StatusListView

app_name = 'statuses'

urlpatterns = [
    path('', StatusListView.as_view(), name='index'),
]
