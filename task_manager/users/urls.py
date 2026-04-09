from django.urls import path

from task_manager.users.views import IndexView

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
