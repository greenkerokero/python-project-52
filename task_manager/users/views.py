from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserCreateForm, UserUpdateForm
from task_manager.users.mixins import UserAccessTestMixin


class UserListView(ListView):
    template_name = 'users/index.html'

    def get_queryset(self):
        return (
            get_user_model()
            .objects.exclude(is_superuser=True)
            .only('username', 'first_name', 'last_name', 'date_joined')
        )


class UserCreateView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')


class UserUpdateView(
    UserAccessTestMixin, SuccessMessageMixin, UpdateView
):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully updated')


class UserDeleteView(
    UserAccessTestMixin, SuccessMessageMixin, DeleteView
):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully removed')
