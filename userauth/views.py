from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm


def login_user(request):
    error_message = ''
    if request.method == 'POST':
        user = get_user_from_request(request)
        if user is None:
            error_message = 'Нет пользователя с таким именем или пароль неверный'
        else:
            login(request, user)
            return redirect('home')
    form = LoginForm()
    data = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'userauth/login.html', data)


def register_user(request):
    error_message = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST["username"])
            user.set_password(request.POST["password"])
            user.save()
            user = get_user_from_request(request)
            login(request, user)
            return redirect('home')
        else:
            error_message = form.errors
    form = RegistrationForm()
    data = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'userauth/registration.html', data)


def logout_user(request):
    logout(request)
    return redirect('home')


def get_user_from_request(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    return user

