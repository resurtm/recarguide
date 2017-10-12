from django.contrib.auth import forms as auth_forms


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.__add_username_attributes()
        self.__add_password_attributes()

    def __add_username_attributes(self):
        old_attrs = self.fields['username'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'aria-describedby': 'login-form-username-help',
                     'placeholder': 'johndoe1970'}
        self.fields['username'].widget.attrs = {**old_attrs, **new_attrs}

    def __add_password_attributes(self):
        old_attrs = self.fields['password'].widget.attrs
        new_attrs = {'class': 'form-control',
                     'placeholder': 's0m3$3cr3tstR1nG'}
        self.fields['password'].widget.attrs = {**old_attrs, **new_attrs}
