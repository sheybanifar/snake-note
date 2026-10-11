from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import Profile

class UserRegistrationViewTests(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testuser',
            'email':    'test@email.com',
            'password': 'strong-password',
            'password2': 'strong-password'
        }

    def test_successful_registration_creates_profile(self):
        response = self.client.post(
            reverse('accounts:register'),
            data=self.form_data
        )

        # assert succeeded registeration
        self.assertRedirects(response, reverse('accounts:user_register_done'))

        User = get_user_model()
        user = User.objects.get(username=self.form_data['username'])

        # assert a profile is found for the user
        self.assertTrue(Profile.objects.filter(user=user).exists())