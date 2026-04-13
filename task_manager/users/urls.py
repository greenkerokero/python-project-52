from django.urls import path

from task_manager.users.views import UserCreateView, UserListView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('<int:pk>/update', UserUpdateView.as_view(), name='update'),
]
