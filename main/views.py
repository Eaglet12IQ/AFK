from django.shortcuts import render

def main(request):
    return render(request, "main.html")

def profile(request):
    return render(request, "profile.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")
