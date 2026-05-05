from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserAccessTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.get_object() == self.request.user
            or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(
            self.request, _('You do not have permission to make changes')
        )
        return redirect('users:index')
