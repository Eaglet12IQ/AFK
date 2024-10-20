from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

def main(request):
    return render(request, "main.html", {'user': request.user})

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "register.html")
    
def events(request):
    if request.user.is_authenticated:
        return render(request, "events.html")
    else:
        return redirect("login")

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "forgot_password.html")

def reset_password(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'user_id': request.user.id}))
    else:
        return render(request, "reset_password.html")