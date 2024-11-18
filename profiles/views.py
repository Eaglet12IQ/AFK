from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import completedTask

def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    user = get_object_or_404(User, id=user_id)
    completedTasks = completedTask.objects.filter(user=request.user)
    context = {
        "nickname": profile.nickname,
        "date_joined": user.date_joined,
        "user_id": user_id,
        "completedTasks": completedTasks
    }
    return render(request, 'profile.html',  context)

def setting(request):
    return render(request, 'setting.html')
