from django.shortcuts import render, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import Tasks
from django.http import JsonResponse
from django.http import HttpResponse
import json

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
            Profile.objects.create(user=user, nickname="Новый пользователь")
            return JsonResponse({"message": "Пользователь зарегистрирован."}, status=201)
        
def admin_users_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
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
    
def admin_users_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        User.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)

def admin_profiles(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        profiles = Profile.objects.all()
        return render(request, "admin-panel-profiles.html", {'profiles': profiles})

def admin_profiles_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        data = json.loads(request.body)
        edit_id = data.get('edit_id')

        nickname = data.get('nickname')

        edit_profile = Profile.objects.get(user_id=edit_id)

        edit_profile.nickname = nickname

        edit_profile.save()

        return JsonResponse({"message": "Данные профиля изменены."}, status=200)

def admin_tasks(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        tasks = Tasks.objects.all()
        return render(request, "admin-panel-tasks.html", {'tasks': tasks})

def admin_tasks_add(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        data = json.loads(request.body)
        description = data.get('description')
        difficulty = data.get('difficulty')
        interest = data.get('interest')

        Tasks.objects.create(description=description, difficulty=difficulty, interest=interest)

        return JsonResponse({"message": "Занятие создано."}, status=201)

def admin_tasks_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        data = json.loads(request.body)
        edit_id = data.get('edit_id')
        description = data.get('description')
        difficulty = data.get('difficulty')
        interest = data.get('interest')

        edit_task = Tasks.objects.get(id=edit_id)

        edit_task.description = description
        edit_task.difficulty = difficulty
        edit_task.interest = interest

        edit_task.save()

        return JsonResponse({"message": "Информация о занятии изменена."}, status=200)
    
def admin_tasks_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        Tasks.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)