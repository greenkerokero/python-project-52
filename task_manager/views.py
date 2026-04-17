from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.info(self.request, _('You are signed in'))
        return super().form_valid(form)


class UserLogoutView(LogoutView):

    def post(self, request, *args, **kwargs):
        messages.info(request, _('You are signed out'))
        return super().post(request, *args, **kwargs)
