from django.urls import path

from task_manager.tasks.views import TasksListView, TasksCreateView

app_name = 'tasks'

urlpatterns = [
    path('', TasksListView.as_view(), name='index'),
    path('create/', TasksCreateView.as_view(), name='create'),
]
