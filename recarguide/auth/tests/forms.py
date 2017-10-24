from bs4 import BeautifulSoup
from django.test import TestCase
from django.utils.crypto import get_random_string

from recarguide.auth.forms import AuthenticationForm, UserCreationForm


class AuthenticationFormTestCase(TestCase):
    def test_adjust_username_field(self):
        f = AuthenticationForm()
        s = BeautifulSoup(str(f['username']), 'html.parser')
        i = s.input

        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['aria-describedby'] == 'login-form-username-help')
        self.assertTrue(i['placeholder'] == 'johndoe1970')

    def test_adjust_password_field(self):
        f = AuthenticationForm()
        s = BeautifulSoup(str(f['password']), 'html.parser')
        i = s.input

        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['placeholder'] == 's0m3$3cr3tstR1nG')


class UserCreationFormTestCase(TestCase):
    def test_email_field(self):
        f = UserCreationForm()
        s = BeautifulSoup(str(f['email']), 'html.parser')
        i = s.input

        self.assertTrue(f.fields['email'].required)
        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['aria-describedby'] == 'signup-form-email-help')
        self.assertTrue(i['placeholder'] == 'john-doe-70@gmail.com')

    def test_adjust_username_field(self):
        f = UserCreationForm()
        s = BeautifulSoup(str(f['username']), 'html.parser')
        i = s.input

        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['aria-describedby'] == 'signup-form-username-help')
        self.assertTrue(i['placeholder'] == 'johndoe1970')

    def test_adjust_password_field(self):
        # password1 field
        f = UserCreationForm()
        s = BeautifulSoup(str(f['password1']), 'html.parser')
        i = s.input

        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['aria-describedby'] == 'signup-form-password1-help')
        self.assertTrue(i['placeholder'] == 's3cr3tp@$$w0rD')

        # password2 field
        f = UserCreationForm()
        s = BeautifulSoup(str(f['password2']), 'html.parser')
        i = s.input

        self.assertTrue('form-control' in i['class'])
        self.assertTrue(i['aria-describedby'] == 'signup-form-password2-help')
        self.assertTrue(i['placeholder'] == 's3cr3tp@$$w0rD')

    def test_save(self):
        password = get_random_string(32)
        data = {'username': get_random_string(32),
                'password1': [password],
                'password2': [password],
                'email': '{}@{}.com'.format(get_random_string(16),
                                            get_random_string(16))}
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(isinstance(user.id, int))
