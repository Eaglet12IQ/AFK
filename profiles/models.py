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

    food_rating = models.PositiveIntegerField(default=0)
    sport_rating = models.PositiveIntegerField(default=0)
    technology_rating = models.PositiveIntegerField(default=0)
    travel_rating = models.PositiveIntegerField(default=0)
    creative_rating = models.PositiveIntegerField(default=0)
    total_rating = models.PositiveIntegerField(default=0, editable=False)  # Храним итог

    def save(self, *args, **kwargs):
        # Перед сохранением обновляем значение total_rating
        self.total_rating = (
            self.food_rating
            + self.sport_rating
            + self.technology_rating
            + self.travel_rating
            + self.creative_rating
        )
        super().save(*args, **kwargs)


    def settings_change(request):
        if request.method == 'POST':
            password = request.POST.get('password')
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')
            profile_picture = request.FILES.get('profile_picture')

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user_id=user)

            if authenticate(username=user.username, password=password):
                user.email = email
                profile.nickname = nickname

                if profile_picture:
                    # Удаляем старую картинку, если нужно
                    if profile.profile_picture and profile.profile_picture.name != 'default_picture.jpg':
                        profile.profile_picture.delete()

                    # Сохраняем новую картинку
                    profile.profile_picture = profile_picture

                user.save()
                profile.save()

                return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': request.user.id})}, status=200)
            else:
                return JsonResponse({"message": "Неверный пароль."}, status=400)