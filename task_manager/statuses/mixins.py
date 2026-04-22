from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class LoginRequiredMessagesMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('You are not authorized'))
        return super().handle_no_permission()
