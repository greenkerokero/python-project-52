from django.views.generic import ListView
from django.contrib.auth import get_user_model


class IndexView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
