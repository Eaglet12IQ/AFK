from authentication.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

def user_register_submit(request):
    return User.register_submit(request)
        
def user_login_submit(request):
    return User.login_submit(request)
        
def user_profile_logout(request, user_id):
    return User.profile_logout(request, user_id)

def user_forgot_password_submit(request):
    return User.forgot_password_submit(request)
            
def user_yandex_auth(request):
    return User.yandex_auth(request)

def user_vk_auth(request):
    return User.vk_auth(request)

def user_vk_auth_submit(request):
    return User.vk_auth_submit(request)

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "login.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "register.html")
    
def forgot_password_view(request):
    return render(request, "forgot_password.html")