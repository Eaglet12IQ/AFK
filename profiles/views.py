from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from profiles.models import Profile

def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    user = get_object_or_404(User, id=user_id)
    context = {
        "nickname": profile.nickname,
        "date_joined": user.date_joined,
        "user_id": user_id,
    }
    return render(request, 'profile.html',  context)

def setting(request):
    return render(request, 'setting.html')
