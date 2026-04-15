from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm


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
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully updated')

    def test_func(self):
        return self.get_object() == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, _('You do not have permission to make changes'))
        return redirect('users:index')


class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully removed')

    def test_func(self):
        return self.get_object() == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, _('You do not have permission to make changes'))
        return redirect('users:index')
