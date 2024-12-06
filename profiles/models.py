from django.db import models
from authentication.models import User
import json
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.TextField(max_length=100)
    profile_picture = models.ImageField(default='default_picture.jpg')

    def settings_change(request):
        data = json.loads(request.body)
        password = data.get('password')
        email = data.get('email')
        nickname = data.get('nickname')
        profile_picture = data.get('profile_picture')

        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user_id=user)

        if authenticate(username=user.username, password=password):
            user.email = email
            profile.nickname = nickname

            user.save()
            profile.save()

            return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': request.user.id})}, status=200)
        else:
            return JsonResponse({"message": "Неверный пароль."}, status=400)