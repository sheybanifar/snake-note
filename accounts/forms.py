from django import forms
from django.contrib.auth import get_user_model

class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Confirm your password.')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

        widgets = {
            'password': forms.PasswordInput
        }

    field_order = [
        'username',
        'password',
        'password2',
        'email'
    ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password2 != password:
            self.add_error(
                'password2',
                'password does not match.')