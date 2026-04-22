from django.urls import path

from task_manager.statuses.views import IndexView

app_name = 'statuses'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
