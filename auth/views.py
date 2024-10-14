from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages

def register_submit(request):
    username = request.POST.get('login').lower()  # Получаем имя пользователя из POST
    password = request.POST.get('password')  # Получаем пароль из POST
    email = request.POST.get('email').lower()

    # Проверяем, существует ли уже пользователь
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Пользователь с таким именем уже существует.')
        return redirect('register')
    elif User.objects.filter(email=email).exists():
        messages.error(request, 'Пользователь с такой почтой уже существует.')
        return redirect('register')

    # Создаем нового пользователя
    user = User.objects.create_user(username=username, password=password, email=email)

    # Аутентифицируем пользователя
    user = authenticate(username=username, password=password, email=email)
    if user is not None:
        login(request, user)  # Вход в систему
        return redirect('profile')  # Перенаправление на профиль
        
def login_submit(request):
    email_username = request.POST.get('email/login').lower()
    password = request.POST.get('password')

    if len(email_username.split("@")) == 2:
        email = email_username
        user = User.objects.get(email=email)
        username = user.username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Вход в систему
            return redirect('profile')  # Перенаправление на профиль
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
        username = email_username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Вход в систему
            return redirect('profile')  # Перенаправление на профиль
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
        
def profile_logout(request):
    logout(request)  # Завершает сессию пользователя
    return redirect('login')  # Перенаправление на страницу входа



    

