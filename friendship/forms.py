from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput


class SearchUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

        widgets = {
            "username": TextInput(attrs={
                'type': "search",
                'class': "form-control rounded",
                'placeholder': "Search",
                'aria-label': "Search",
                'aria-describedby': "search-addon"
            })
        }


class ViewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            "username": TextInput(attrs={
                'type': 'text',
                'class': 'form-control-plaintext',
                'placeholder': 'Username',
                'readonly': True,
            }),
            "email": EmailInput(attrs={
                'type': 'text',
                'class': 'form-control-plaintext',
                'placeholder': '',
                'readonly': True,
            }),
        }
