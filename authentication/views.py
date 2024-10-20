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
        Profile.objects.create(user=user, nickname="Новый пользователь")
        return redirect(reverse('profile', kwargs={'user_id': user.id}))  # Перенаправление на профиль
        
def login_submit(request):
    email_username = request.POST.get('email/login').lower()
    password = request.POST.get('password')
    remember_me = request.POST.get('remember_me')

    if len(email_username.split("@")) == 2:
        email = email_username
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
        username = user.username
    else:
        username = email_username

    user = authenticate(username=username, password=password)
    if user is not None:
        if remember_me:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)
        login(request, user)  # Вход в систему
        return redirect(reverse('profile', kwargs={'user_id': user.id}))  # Перенаправление на профиль
    else:
        messages.error(request, 'Invalid email or password.')
        return redirect('login')
        
def profile_logout(request, user_id):
    logout(request)  # Завершает сессию пользователя
    return redirect('login')  # Перенаправление на страницу входа

def forgot_password_submit(request):

    def send_confirmation_email(email, confirmation_code):
        subject = 'Email Confirmation'
        message = f'Your confirmation code is: {confirmation_code}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

    if request.method == "POST":
        email = request.POST.get('email').lower()
        code = request.POST.get('code')
        if code is None:
            try:
                user = User.objects.get(email=email)
                confirmation_code = uuid.uuid4()
                PasswordResetCode.objects.create(user=user, code=confirmation_code)
                send_confirmation_email(email, confirmation_code)
                return JsonResponse({"message": "Код отправлен."}, status=200)
            except User.DoesNotExist:
                return JsonResponse({"message": "Пользователя с такой почтой не существует."}, status=400)
        else:
            user = User.objects.get(email=email)
            password_reset_codes = PasswordResetCode.objects.filter(user_id=user.id)
            last_code = PasswordResetCode.objects.filter(user_id=user.id).order_by('-id').first().code
            if password_reset_codes.filter(code=code).exists() and code == last_code:
                PasswordResetCode.objects.filter(user_id=user.id).delete()
                return JsonResponse({"redirect_url": "reset_password/"}, status=200)
            else:
                return JsonResponse({"message": "Код неверен либо устарел."}, status=400)