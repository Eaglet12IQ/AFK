from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import completedTask

def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    user = get_object_or_404(User, id=user_id)
    completedTasks = completedTask.objects.filter(user=user_id)
    context = {
        "nickname": profile.nickname,
        "date_joined": user.date_joined,
        "user_id": user_id,
        "completedTasks": completedTasks,
        "profile_picture": profile.profile_picture
    }
    return render(request, 'profile.html',  context)

def settings_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    user = get_object_or_404(User, id=user_id)
    context = {
        "nickname": profile.nickname,
        "email": user.email,
        "profile_picture": profile.profile_picture
    }
    return render(request, 'settings.html', context)

def profile_settings_change(request, user_id):
    return Profile.settings_change(request)
