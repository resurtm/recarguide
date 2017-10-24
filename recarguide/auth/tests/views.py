import re

from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string


class SignupViewTestCase(TestCase):
    def test_signup1(self):
        resp = self.client.get(reverse('auth:signup'))
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode('utf-8', 'strict')
        self.assertIsNotNone(re.search('<h1[^>]*>Create Account</h1>', content))
        self.assertIsNotNone(re.search('<button[^>]*>Register</button>',
                                       content))

    def test_signup2(self):
        password = get_random_string(32)
        data = {'username': get_random_string(32),
                'password1': [password],
                'password2': [password],
                'email': '{}@{}.com'.format(get_random_string(16),
                                            get_random_string(16))}

        resp = self.client.post(reverse('auth:signup'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('location' in resp)
        self.assertEqual(resp['location'], '/login/')

    def test_signup3(self):
        resp = self.client.post(reverse('auth:signup'), {})
        self.assertEqual(resp.status_code, 200)
