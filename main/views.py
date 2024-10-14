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
