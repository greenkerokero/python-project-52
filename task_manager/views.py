from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.info(self.request, 'You are signed in')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'

    def post(self, request, *args, **kwargs):
        messages.info(request, 'You are signed out')
        return super().post(request, *args, **kwargs)
