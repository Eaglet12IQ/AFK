from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profiles.models import Profile
from django.http import JsonResponse

def admin_users(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        users = User.objects.all()
        return render(request, "admin-panel-users.html", {'users': users})
    
def admin_users_add(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
        
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)
        
        password = request.POST.get('password')
        is_superuser = request.POST.get('is_superuser')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff')
        is_active = request.POST.get('is_active')
        first_name = request.POST.get('first_name')

        user = User.objects.create_user(username=username, password=password, email=email, is_superuser=is_superuser, last_name=last_name, is_staff=is_staff, is_active=is_active, first_name=first_name)

        # Аутентифицируем пользователя
        if user is not None:
            Profile.objects.create(user=user, nickname="Новый пользователь")
            return JsonResponse({"message": "Пользователь зарегистрирован."}, status=200)

def admin_profiles(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        profiles = Profile.objects.all()
        return render(request, "admin-panel-profiles.html", {'profiles': profiles})

def admin_tasks(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return render(request, "admin-panel-tasks.html")
