from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True,
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com',
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': True,
            })
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True,
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': True,
            })
        }
