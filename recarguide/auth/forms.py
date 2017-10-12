from django.contrib.auth import forms


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
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.__adjust_username_field()

    def __adjust_username_field(self):
        old_attrs = self.fields['username'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'aria-describedby': 'login-form-username-help',
                     'placeholder': 'johndoe1970'}
        self.fields['username'].widget.attrs = {**old_attrs, **new_attrs}
