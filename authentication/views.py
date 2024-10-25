from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from profiles.models import Profile
from django.http import JsonResponse
from django.core.mail import send_mail
import uuid
from django.conf import settings
from authentication.models import PasswordResetCode
import threading

def register_submit(request):
    if request.method == "POST":
        email = request.POST.get('email').lower()
        loginStr = request.POST.get('login').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            # Проверяем, существует ли уже пользователь
            if User.objects.filter(username=login).exists():
                return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
            elif User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)

            # Создаем нового пользователя
            user = User.objects.create_user(username=loginStr, password=password1, email=email)

            # Аутентифицируем пользователя
            user = authenticate(username=loginStr, password=password1, email=email)
            if user is not None:
                login(request, user)  # Вход в систему
                Profile.objects.create(user=user, nickname="Новый пользователь")
                return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user.id})}, status=200)
        else:
            return JsonResponse({"message": "Пароли не совпадают."}, status=400)
        
def login_submit(request):
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

    def send_confirmation_email(email, confirmation_code):
        subject = 'Email Confirmation'
        message = f'Your confirmation code is: {confirmation_code}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        threading.Thread(target=send_mail, args=(subject, message, email_from, recipient_list)).start()

    if request.method == "POST":
        email = request.POST.get('email').lower()
        code = request.POST.get('code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if code is None and email is not None and password1 is None and password2 is None:
            try:
                user = User.objects.get(email=email)
                confirmation_code = uuid.uuid4()
                PasswordResetCode.objects.create(user=user, code=confirmation_code)
                send_confirmation_email(email, confirmation_code)
                return JsonResponse({"message": "Код отправлен."}, status=200)
            except User.DoesNotExist:
                return JsonResponse({"message": "Пользователя с такой почтой не существует."}, status=400)
        elif code is not None and email is not None and password1 is None and password2 is None:
            user = User.objects.get(email=email)
            password_reset_codes = PasswordResetCode.objects.filter(user_id=user.id)
            last_code = PasswordResetCode.objects.filter(user_id=user.id).order_by('-id').first().code
            if password_reset_codes.filter(code=code).exists() and code == last_code:
                PasswordResetCode.objects.filter(user_id=user.id).delete()
                return JsonResponse({"message": "Код подтвержден."}, status=200)
            else:
                return JsonResponse({"message": "Код неверен либо устарел."}, status=400) 
        else:
            if password1 != password2:
                return JsonResponse({"message": "Пароли не совпадают."}, status=400)
            else:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                login(request, user)
                return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user.id})}, status=200)