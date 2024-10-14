from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from profiles.models import Profile

def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    return render(request, 'profile.html',  {'profile': profile})
