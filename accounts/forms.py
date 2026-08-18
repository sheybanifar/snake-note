from django import forms
from django.contrib.auth import get_user_model

class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

    field_order = [
        'username',
        'password',
        'password2',
        'email'
    ]