from django.shortcuts import render
from django.contrib.auth.models import User

def main(request):
    return render(request, "main.html")

def profile(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    else:
        return render(request, "profile.html")

def login(request):
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return render(request, "login.html")

def register(request):
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return render(request, "register.html")
