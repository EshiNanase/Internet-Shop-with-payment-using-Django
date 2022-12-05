from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.models import User
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import Basket


def login(request):
    title = 'Store - Авторизация'
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to=reverse('index'))
            else:
                context = {'form': form}
                return render(request, 'users/login.html', context)
    else:
        form = UserLoginForm()
    context = {'form': form,
               'title': title}
    return render(request, 'users/login.html', context)


def register(request):
    title = 'Store - Регистрация'
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистровались')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form,
               'title': title}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    title = 'Личный кабинет'
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': title,
               'form': form,
               'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

