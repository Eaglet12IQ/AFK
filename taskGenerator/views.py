from taskGenerator.models import Tasks
from taskGenerator.models import completedTask
from django.shortcuts import render, redirect

def tasks_idea_generation(request):
    return Tasks.idea_generation(request)

def events_view(request):
    if request.user.is_authenticated:
        completedTasks = completedTask.objects.filter(user=request.user).order_by('-id')[:10]
        context = {
            "completedTasks": completedTasks
        }
        return render(request, "events.html", context)
    else:
        return redirect("login")
