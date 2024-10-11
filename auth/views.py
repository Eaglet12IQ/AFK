from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def register_submit(request):
    username = request.POST.get('login')  # Получаем имя пользователя из POST
    password = request.POST.get('password')  # Получаем пароль из POST
    email = request.POST.get('email')

    # Проверяем, существует ли уже пользователь
    if User.objects.filter(username=username).exists():
        return render(request, 'register.html', {'error': 'Пользователь с таким именем уже существует.'})
    elif User.objects.filter(email=email).exists():
        return render(request, 'register.html', {'error': 'Пользователь с такой почтой уже существует.'})

    # Создаем нового пользователя
    user = User.objects.create_user(username=username, password=password, email=email)

    # Аутентифицируем пользователя
    user = authenticate(username=username, password=password, email=email)
    if user is not None:
        login(request, user)  # Вход в систему
        return redirect('profile')  # Перенаправление на профиль
        
def login_submit(request):
    email_username = request.POST.get('email/login')
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
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    else:
        username = email_username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Вход в систему
            return redirect('profile')  # Перенаправление на профиль
        else:
            return render(request, 'login.html', {'error': 'Invalid login or password.'})



    

