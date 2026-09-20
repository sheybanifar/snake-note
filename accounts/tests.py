from django.test import TestCase
from django.urls import reverse

class LoginTest(TestCase):
    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'Kian',
                'password': 'kian12345'
            },
        )

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('accounts:dashboard'))

    def test_login_with_invalid_password(self):
        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'Kian',
                'password': 'wrong-password'
            },
        )

        self.assertNotEqual(response.status_code, 302)