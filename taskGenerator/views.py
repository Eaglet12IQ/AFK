from taskGenerator.models import Tasks
from django.shortcuts import render, redirect

def tasks_idea_generation(request):
    return Tasks.idea_generation(request)

def events_view(request):
    if request.user.is_authenticated:
        return render(request, "events.html")
    else:
        return redirect("login")
