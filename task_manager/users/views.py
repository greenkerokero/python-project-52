from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model


class UserListView(ListView):
    template_name = 'users/index.html'

    def get_queryset(self):
        return get_user_model().objects.only('username', 'first_name', 'last_name', 'date_joined')
