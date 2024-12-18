from django.db import models
from django.shortcuts import render, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import Tasks
from django.http import HttpResponse, JsonResponse
import json

class Admin(models.Model):
    def users_add(request):
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
        
    def users_edit(request):
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
        
    def users_delete(request):
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        User.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)

    def profiles_edit(request):
        data = json.loads(request.body)
        edit_id = data.get('edit_id')

        nickname = data.get('nickname')

        profile_picture = data.get('profile_picture')

        edit_profile = Profile.objects.get(user_id=edit_id)

        edit_profile.nickname = nickname
        edit_profile.profile_picture = profile_picture

        edit_profile.save()

        return JsonResponse({"message": "Данные профиля изменены."}, status=200)

    def tasks_add(request):
        data = json.loads(request.body)
        description = data.get('description')
        difficulty = data.get('difficulty')
        interest = data.get('interest')

        Tasks.objects.create(description=description, difficulty=difficulty, interest=interest)

        return JsonResponse({"message": "Занятие создано."}, status=201)

    def tasks_edit(request):
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
        
    def tasks_delete(request):
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        Tasks.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)
