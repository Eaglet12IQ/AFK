from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from profiles.models import Profile
from taskGenerator.models import completedTask

def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    user = get_object_or_404(User, id=user_id)
    completedTasks = completedTask.objects.filter(user=user_id)

    # Преобразуем дату выполнения задач с проверкой на None
    formatted_completedTasks = []
    for task in completedTasks:
        if task.completed_when:  # Проверяем, что дата не None
            task.completed_when = task.completed_when.strftime('%d %B %Y')  # Форматируем дату
        formatted_completedTasks.append(task)

    context = {
        "nickname": profile.nickname,
        "date_joined": user.date_joined.strftime('%d %B %Y') if user.date_joined else "Дата не указана",  # Проверяем дату регистрации
        "user_id": user_id,
        "completedTasks": formatted_completedTasks,  # Передаем отформатированные задачи
        "profile_picture": profile.profile_picture,
        "completedTask_count": completedTasks.filter(confirmed="Yes").count(),
    }
    return render(request, 'profile.html', context)


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
