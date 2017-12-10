from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.forms import EmailField, EmailInput

from django.template.loader import render_to_string
from django.core.mail import send_mail

class AuthenticationForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.__adjust_username_field()
        self.__adjust_password_field()

    def __adjust_username_field(self):
        old_attrs = self.fields['username'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'aria-describedby': 'login-form-username-help',
                     'placeholder': 'johndoe1970'}
        self.fields['username'].widget.attrs = {**old_attrs, **new_attrs}

    def __adjust_password_field(self):
        old_attrs = self.fields['password'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'placeholder': 's0m3$3cr3tstR1nG'}
        self.fields['password'].widget.attrs = {**old_attrs, **new_attrs}


class UserCreationForm(forms.UserCreationForm):
    email = EmailField(
        required=True,
        widget=EmailInput(
            attrs={'class': 'form-control',
                   'aria-describedby': 'signup-form-email-help',
                   'placeholder': 'john-doe-70@gmail.com'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': forms.UsernameField, 'email': EmailField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.__adjust_username_field()
        self.__adjust_password_field(1)
        self.__adjust_password_field(2)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
        self.__send_signup_email(user)
        return user

    def __send_signup_email(self, user):
        html = render_to_string('registration/signup_email.html', {
            'user': user,
        })
        send_mail(
            'ReCarGuide — verify your email',
            html,
            'resurtm@gmail.com',
            [user.email],
            fail_silently=False,
        )

    def __adjust_username_field(self):
        old_attrs = self.fields['username'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'aria-describedby': 'signup-form-username-help',
                     'placeholder': 'johndoe1970'}
        self.fields['username'].widget.attrs = {**old_attrs, **new_attrs}

    def __adjust_password_field(self, num):
        name = 'password{}'.format(str(num))
        old_attrs = self.fields[name].widget.attrs
        new_attrs = {'class': 'form-control',
                     'aria-describedby': 'signup-form-{}-help'.format(name),
                     'placeholder': 's3cr3tp@$$w0rD'}
        self.fields[name].widget.attrs = {**old_attrs, **new_attrs}
