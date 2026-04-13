from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm


class UserListView(ListView):
    template_name = 'users/index.html'

    def get_queryset(self):
        return get_user_model().objects.exclude(is_superuser=True).only(
            'username', 'first_name', 'last_name', 'date_joined'
        )


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:index')  # replace 'users:list' to 'login'


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')


class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
