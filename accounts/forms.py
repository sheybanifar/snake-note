from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Confirm your password.')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

        widgets = {
            'password': forms.PasswordInput,
            'email': forms.EmailInput({'required': True})
        }

    field_order = [
        'username',
        'password',
        'password2',
        'email'
    ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(
                'This email already is taken. try another.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password2 != password:
            self.add_error(
                'password2',
                'password does not match.')