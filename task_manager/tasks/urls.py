from django.urls import path

from task_manager.tasks.views import TasksListView

app_name = 'tasks'

urlpatterns = [
    path('', TasksListView.as_view(), name='index'),
]
