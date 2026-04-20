from django.forms import ModelForm
from django.contrib.auth import get_user_model, forms
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']


class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
