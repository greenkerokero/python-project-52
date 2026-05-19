from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class LoginRequiredMessagesMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized'))
        return super().handle_no_permission()


class UserAccessTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_message = ''
    permission_url = ''

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if hasattr(obj, 'reporter'):
            return obj.reporter == user or user.is_superuser

        return obj == user or user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)
