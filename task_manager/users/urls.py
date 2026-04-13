from django.urls import path

from task_manager.users.views import UserListView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
]
