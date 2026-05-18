from django.urls import path

from task_manager.users.views import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
    UserPasswordChangeView,
)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/password/', UserPasswordChangeView.as_view(),
         name='password_change'),
]
