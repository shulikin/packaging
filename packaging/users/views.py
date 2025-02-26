# import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import render
from .forms import LoginUserForm
from users.models import Client, User


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('registration:index')
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')


def personal_account_user(request, user_id):
    account_user = get_object_or_404(User, pk=user_id)
    context = {
        'button_class': 'btn btn-success',
        'account_user': account_user,
    }
    return render(request, 'users/personal_account.html', context)
