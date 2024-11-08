from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import Profile
from django.http import JsonResponse
from django.core.cache import cache
import requests
from AFK.utils.password_check import password_check
from AFK.utils.confirmation import send_confirmation_email
from AFK.utils.confirmation import generate_numeric_code
import json

def register_submit(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        loginStr = request.POST.get('login').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        code = request.POST.get('code')

        if code is None:
            if password1 == password2:

                check = password_check(password1)

                if check:
                    return check

                # Проверяем, существует ли уже пользователь
                if User.objects.filter(username=loginStr).exists():
                    return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)
                
                confirmation_code = generate_numeric_code()
                cache.set(email, confirmation_code, timeout=300)
                send_confirmation_email(email, confirmation_code)
                return JsonResponse({"message": "Код отправлен."}, status=202)
            else:
                return JsonResponse({"message": "Пароли не совпадают."}, status=400)
        else:
            confirmation_code = cache.get(email)
            if code == confirmation_code:
                cache.delete(email)
                # Создаем нового пользователя
                user = User.objects.create_user(username=loginStr, password=password1, email=email)

                # Аутентифицируем пользователя
                if user is not None:
                    login(request, user)  # Вход в систему
                    Profile.objects.create(user=user, nickname="Новый пользователь")
                    return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user.id})}, status=200)
            else:
                return JsonResponse({"message": "Код неверен либо устарел."}, status=400) 
        
def login_submit(request):
    if request.method == "GET":
        code = request.GET.get('code')
        token_url = 'https://oauth.yandex.ru/token'
        
        # Получение токена
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': "2f83d1ed7ab94e6f9b01785af3282327",
            'client_secret': "669d976630fa409cbd99d3d01d9f5d5f",
            'redirect_uri': "http://127.0.0.1:8000/login/submit_form/",
        }
        
        response = requests.post(token_url, data=data)
        token_info = response.json()
        access_token = token_info.get('access_token')

        # Используйте access_token для получения информации о пользователе
        user_info_url = 'https://login.yandex.ru/info'
        headers = {'Authorization': f'OAuth {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        loginStr = user_info.get('login')
        email = user_info.get('default_email')
        try:
            user = User.objects.get(email=email)
            login(request, user)
            return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
        except User.DoesNotExist:
            user = User.objects.create_user(username=loginStr, email=email)
            login(request, user)  # Вход в систему
            Profile.objects.create(user=user, nickname="Новый пользователь")
            return redirect(reverse('profile', kwargs={'user_id': request.user.id}))

    if request.method == "POST":
        emailLogin = request.POST.get('emailLogin').lower()
        password = request.POST.get('password')
        rememberMe = request.POST.get('rememberMe')

        if len(emailLogin.split("@")) == 2:
            email = emailLogin
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"message": "Invalid email or password."}, status=400)
            username = user.username
        else:
            username = emailLogin

        user = authenticate(username=username, password=password)
        if user is not None:
            if rememberMe:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            login(request, user)  # Вход в систему
            return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user.id})}, status=200)
        else:
            return JsonResponse({"message": "Invalid email or password."}, status=400)
        
def profile_logout(request, user_id):
    logout(request)  # Завершает сессию пользователя
    return redirect('login')  # Перенаправление на страницу входа

def forgot_password_submit(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Десериализация JSON
        email = data.get('email').lower()
        code = data.get('code')
        if code is None:
            try:
                user = User.objects.get(email=email)
                confirmation_code = generate_numeric_code()
                cache.set(email, confirmation_code, timeout=300)
                send_confirmation_email(email, confirmation_code)
                return JsonResponse({"message": "Код отправлен."}, status=202)
            except User.DoesNotExist:
                return JsonResponse({"message": "Пользователя с такой почтой не существует."}, status=400)
        else:
            confirmation_code = cache.get(email)
            if code == confirmation_code:
                cache.delete(email)
                return JsonResponse({"message": "Код подтвержден."}, status=202)
            else:
                return JsonResponse({"message": "Код неверен либо устарел."}, status=400) 
    if request.method == "PATCH":
        data = json.loads(request.body)  # Десериализация JSON
        email = data.get('email').lower()
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            return JsonResponse({"message": "Пароли не совпадают."}, status=400)
        else:
            check = password_check(password1)
            if check:
                return check
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            login(request, user)
            return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user.id})}, status=200)
            
def yandex_auth(request):
    # URL для авторизации
    auth_url = 'https://oauth.yandex.ru/authorize'
    params = {
        'response_type': 'code',
        'client_id': "2f83d1ed7ab94e6f9b01785af3282327",
    }
    return redirect(f"{auth_url}?{requests.compat.urlencode(params)}")