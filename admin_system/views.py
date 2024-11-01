from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profiles.models import Profile
from taskGenerator.models import Tasks
from django.http import JsonResponse
from django.http import HttpResponse

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
            return JsonResponse({"message": "Пользователь зарегистрирован."}, status=201)
        
def admin_users_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        edit_id = request.POST.get('edit_id')

        username = request.POST.get('username')
        if User.objects.filter(username=username).exclude(id=edit_id).exists():
            return JsonResponse({"message": "Пользователь с таким именем уже существует."}, status=400)
        
        email = request.POST.get('email')
        if User.objects.filter(email=email).exclude(id=edit_id).exists():
            return JsonResponse({"message": "Пользователь с такой почтой уже существует."}, status=400)
        
        is_superuser = request.POST.get('is_superuser')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff')
        is_active = request.POST.get('is_active')
        first_name = request.POST.get('first_name')

        edit_user = User.objects.get(id=edit_id)

        edit_user.username = username
        edit_user.email = email
        edit_user.is_superuser = is_superuser
        edit_user.last_name = last_name
        edit_user.is_staff = is_staff
        edit_user.is_active = is_active
        edit_user.first_name = first_name

        edit_user.save()

        return JsonResponse({"message": "Данные пользователя изменены."}, status=200)
    
def admin_users_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        delete_id = request.POST.get('delete_id')

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
        edit_id = request.POST.get('edit_id')

        nickname = request.POST.get('nickname')

        edit_profile = Profile.objects.get(id=edit_id)

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
        description = request.POST.get('description')
        difficulty = request.POST.get('difficulty')
        interest = request.POST.get('interest')

        Tasks.objects.create(description=description, difficulty=difficulty, interest=interest)

        return JsonResponse({"message": "Занятие создано."}, status=201)

def admin_tasks_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        edit_id = request.POST.get('edit_id')
        description = request.POST.get('description')
        difficulty = request.POST.get('difficulty')
        interest = request.POST.get('interest')

        edit_task = Tasks.objects.get(id=edit_id)

        edit_task.description = description
        edit_task.difficulty = difficulty
        edit_task.interest = interest

        edit_task.save()

        return JsonResponse({"message": "Данные занятия изменены."}, status=200)
    
def admin_tasks_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        delete_id = request.POST.get('delete_id')

        Tasks.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)