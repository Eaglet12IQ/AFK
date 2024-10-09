from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def register(request):
    username = request.POST.get('login')  # Получаем имя пользователя из POST
    password = request.POST.get('password')  # Получаем пароль из POST
    email = request.POST.get('email')

    # Проверяем, что имя пользователя и пароль заданы
    if username and password:
        # Проверяем, существует ли уже пользователь
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Пользователь с таким именем уже существует.'})

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, password=password, email=email)

        # Аутентифицируем пользователя
        user = authenticate(username=username, password=password, email=email)
        if user is not None:
            login(request, user)  # Вход в систему
            return redirect('profile')  # Перенаправление на профиль

