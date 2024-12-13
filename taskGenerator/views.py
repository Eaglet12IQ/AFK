from taskGenerator.models import Tasks
from taskGenerator.models import completedTask, confirmationTask
from django.shortcuts import render, redirect

def tasks_idea_generation(request):
    return Tasks.idea_generation(request)

def confirmationTask_confirmation_task(request, user_id):
    return confirmationTask.confirmation_task(request)

def events_view(request):
    if request.user.is_authenticated:
        completedTasks = completedTask.objects.filter(user=request.user).order_by('-id')[:10]
        context = {
            "completedTasks": completedTasks
        }
        return render(request, "events.html", context)
    else:
        return redirect("login")
