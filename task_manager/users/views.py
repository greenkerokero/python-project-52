from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
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


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.get_object() == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, "You do not have permission")
        return redirect('users:index')


class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
