from django.shortcuts import render, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import Tasks
from notification.models import Notification
from taskGenerator.models import confirmationTask

def users_view(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        users = User.objects.all()
        return render(request, "admin-panel-users.html", {'users': users})
    
def admin_users_add(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return User.users_add(request)
        
def admin_users_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return User.users_edit(request)
    
def admin_users_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return User.users_delete(request)

def profiles_view(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        profiles = Profile.objects.all()
        return render(request, "admin-panel-profiles.html", {'profiles': profiles})

def admin_profiles_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Profile.profiles_edit(request)

def tasks_view(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        tasks = Tasks.objects.all()
        return render(request, "admin-panel-tasks.html", {'tasks': tasks})

def admin_tasks_add(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Tasks.tasks_add(request)

def admin_tasks_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Tasks.tasks_edit(request)
    
def admin_tasks_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Tasks.tasks_delete(request)
    
def notifications_view(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        notifications = Notification.objects.filter(checked=False)
        return render(request, "admin-panel-notifications.html",{'notifications': notifications})
    
def admin_notifications_add(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Notification.notifications_add(request) 
    
def admin_notifications_edit(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Notification.notifications_edit(request)
    
def admin_notifications_delete(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return Notification.notifications_delete(request)
    
def confirmations_view(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect("main")
    else:
        confirmations = confirmationTask.objects.filter(confirmed=None)
        return render(request, "admin-panel-confirmations.html",{'confirmations': confirmations})
    
def confirmations_accept(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return confirmationTask.confirmations_accept(request)
    
def confirmations_refuse(request):
    if not request.user.is_superuser:
        return redirect("main")
    else:
        return confirmationTask.confirmations_refuse(request)