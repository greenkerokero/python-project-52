from django.urls import path

from task_manager.tasks.views import TaskCreateView, TaskListView, TaskUpdateView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
]
