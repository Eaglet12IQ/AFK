from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from AFK.utils.password_check import password_check
from AFK.utils.confirmation import send_confirmation_email
from AFK.utils.confirmation import generate_numeric_code
import json
import requests

class User(AbstractUser):
    first_name = None
    last_name = None
    groups = None
    user_permissions = None

    def register_submit(request):
        if request.method == "POST":
            data = json.loads(request.body)  # Десериализация JSON
            email = data.get('email')
            loginStr = data.get('login')
            password1 = data.get('password1')
            password2 = data.get('password2')
            code = data.get('code')

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
                        from profiles.models import Profile
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
                from profiles.models import Profile
                Profile.objects.create(user=user, nickname="Новый пользователь")
                return redirect(reverse('profile', kwargs={'user_id': request.user.id}))

        if request.method == "POST":
            data = json.loads(request.body)  # Десериализация JSON
            emailLogin = data.get('emailLogin')
            password = data.get('password')
            rememberMe = data.get('rememberMe')

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
            email = data.get('email')
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
            email = data.get('email')
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
    
    def users_add(request):
        data = json.loads(request.body)
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
        
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)
        
        password = data.get('password')
        is_superuser = data.get('is_superuser')
        is_staff = data.get('is_staff')
        is_active = data.get('is_active')

        user = User.objects.create_user(username=username, password=password, email=email, is_superuser=is_superuser, is_staff=is_staff, is_active=is_active)

        # Аутентифицируем пользователя
        if user is not None:
            from profiles.models import Profile
            Profile.objects.create(user=user, nickname="Новый пользователь")
            return JsonResponse({"message": "Пользователь зарегистрирован."}, status=201)
        
    def users_edit(request):
        data = json.loads(request.body)
        edit_id = data.get('edit_id')

        username = data.get('username')
        if User.objects.filter(username=username).exclude(id=edit_id).exists():
            return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
        
        email = data.get('email')
        if User.objects.filter(email=email).exclude(id=edit_id).exists():
            return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)
        
        is_superuser = data.get('is_superuser')
        is_staff = data.get('is_staff')
        is_active = data.get('is_active')

        edit_user = User.objects.get(id=edit_id)

        edit_user.username = username
        edit_user.email = email
        edit_user.is_superuser = is_superuser
        edit_user.is_staff = is_staff
        edit_user.is_active = is_active

        edit_user.save()

        return JsonResponse({"message": "Данные пользователя изменены."}, status=200)
    
    def users_delete(request):
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        User.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)

    def vk_auth(request):
        # URL для авторизации
        auth_url = 'https://oauth.vk.com/authorize'
        params = {
            'client_id': '52871021',  # Замените на ID вашего приложения VK
            'redirect_uri': 'https://127.0.0.1:8000/login/vk/submit/',  # Замените на ваш redirect_uri
            'display': 'page',
            'scope': 'email',  # Укажите нужные права доступа
            'response_type': 'code',
            'v': '5.131'  # Версия API VK
        }
        return redirect(f"{auth_url}?{requests.compat.urlencode(params)}")
    
    def vk_auth_submit(request):
        if request.method == "GET":
            code = request.GET.get('code')  # Получаем код авторизации от VK
            token_url = 'https://oauth.vk.com/access_token'

            # Получение токена
            data = {
                'client_id': '52871021',  # Замените на ID вашего приложения VK
                'client_secret': '7d93fc417d93fc417d93fc41fa7eb5432c77d937d93fc411af7b71145a3fbc4660cc718',  # Замените на Secret вашего приложения VK
                'redirect_uri': 'https://127.0.0.1:8000/login/vk/submit/',  # Должен совпадать с redirect_uri в приложении
                'code': code,
            }

            response = requests.get(token_url, params=data)
            token_info = response.json()
            access_token = token_info.get('access_token')
            email = token_info.get('email')  # Email доступен только при запросе scope=email
            user_id = token_info.get('user_id')

            # Получение информации о пользователе из VK
            user_info_url = 'https://api.vk.com/method/users.get'
            user_info_params = {
                'user_ids': user_id,
                'fields': 'photo_max',  # Укажите нужные поля (например, фото профиля)
                'access_token': access_token,
                'v': '5.131'
            }
            user_info_response = requests.get(user_info_url, params=user_info_params)
            user_info = user_info_response.json()
            user_data = user_info.get('response', [])[0]  # Получаем первый элемент списка

            loginStr = user_data.get('first_name') + "_" + user_data.get('last_name')
            try:
                user = User.objects.get(email=email)
                login(request, user)
                return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
            except User.DoesNotExist:
                user = User.objects.create_user(username=loginStr, email=email)
                login(request, user)  # Вход в систему
                from profiles.models import Profile
                Profile.objects.create(user=user, nickname="Новый пользователь")
                return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
