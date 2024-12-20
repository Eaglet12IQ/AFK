from django.db import models
from django.http import JsonResponse, HttpResponse
import json
import random
from typing import Dict, Union
from authentication.models import User
from profiles.models import Profile
from notification.models import Notification
from django.urls import reverse
from datetime import date

class Tasks(models.Model):
    description = models.TextField(max_length=100)
    difficulty = models.TextField(max_length=10)
    interest = models.TextField(max_length=30)

    def tasks_add(request):
        data = json.loads(request.body)
        description = data.get('description')
        difficulty = data.get('difficulty')
        interest = data.get('interest')

        Tasks.objects.create(description=description, difficulty=difficulty, interest=interest)

        return JsonResponse({"message": "Занятие создано."}, status=201)
    
    def tasks_edit(request):
        data = json.loads(request.body)
        edit_id = data.get('edit_id')
        description = data.get('description')
        difficulty = data.get('difficulty')
        interest = data.get('interest')

        edit_task = Tasks.objects.get(id=edit_id)

        edit_task.description = description
        edit_task.difficulty = difficulty
        edit_task.interest = interest

        edit_task.save()

        return JsonResponse({"message": "Информация о занятии изменена."}, status=200)
    
    def tasks_delete(request):
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        Tasks.objects.filter(id=delete_id).delete()

        return HttpResponse(status=200)

    def idea_generation(request):
        interests = json.loads(request.GET.get('interests'))
        difficulty = json.loads(request.GET.get('difficulty'))

        from taskGenerator.models import completedTask
        last_generations_id_list = [gen.task.id for gen in completedTask.objects.filter(user=request.user)]

        if not interests and not difficulty:
            tasks = Tasks.objects.filter().exclude(id__in=last_generations_id_list)
        elif not interests:
            tasks = Tasks.objects.filter(difficulty__in=difficulty).exclude(id__in=last_generations_id_list)
        elif not difficulty:
            tasks = Tasks.objects.filter(interest__in=interests).exclude(id__in=last_generations_id_list)
        else:
            tasks = Tasks.objects.filter(difficulty__in=difficulty, interest__in=interests).exclude(id__in=last_generations_id_list)

        if not tasks:
            return JsonResponse({"message": "Задания закончились("}, status=400)

        random_task = random.choice(tasks)

        completedTask.objects.create(task=random_task, user=request.user)

        completed_task: Dict[str, Union[int, str]] = {
            "task_id": random_task.id,
            "task_description": random_task.description,
            "tasks_count": len(completedTask.objects.filter(user=request.user))
        }

        return JsonResponse(completed_task, status=200)
    
class completedTask(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_when = models.DateTimeField(blank=True, null=True)
    confirmed = models.CharField(max_length=10, default='No')

class confirmationTask(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmation_tasks_as_user')  # Связь с пользователем как "инициатор"
    doer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='confirmation_tasks_as_doer')  # Связь с пользователем как "исполнитель"
    file = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=100)
    confirmed = models.BooleanField(blank=True, null=True)

    def confirmation_task(request):
        task_id = request.POST.get('task_id')
        user_id = request.POST.get('user_id')
        confirmation_file = request.FILES.get('confirmation')
        description = request.POST.get('description')

        task = Tasks.objects.get(id=task_id)
        completed_task = completedTask.objects.get(task=task_id)
        user = User.objects.get(id=user_id)

        confirmationTask.objects.create(task=task, user=user, file=confirmation_file, description=description)
        completed_task.confirmed = "Pending"

        completed_task.save()

        return JsonResponse({"redirect_url": reverse('profile', kwargs={'user_id': user_id})}, status=200)
    
    def confirmations_refuse(request):
        data = json.loads(request.body)
        refuse_id = data.get('refuse_id')

        refuse_task = confirmationTask.objects.get(id=refuse_id)
        completed_task = completedTask.objects.get(task=refuse_task.task, user=refuse_task.user)

        completed_task.confirmed = "No"
        completed_task.save()

        Notification.objects.create(user=refuse_task.user, description=f"Ваша заявка на подтверждение {refuse_task.task.id} задания была отклонена!")

        refuse_task.confirmed = False
        refuse_task.doer = request.user
        refuse_task.save()

        return HttpResponse(status=200)
    
    def confirmations_accept(request):
        data = json.loads(request.body)
        accept_id = data.get('accept_id')

        accept_task = confirmationTask.objects.get(id=accept_id)
        completed_task = completedTask.objects.get(task=accept_task.task, user=accept_task.user)

        completed_task.confirmed = "Yes"
        completed_task.completed_when = date.today()
        completed_task.save()

        Notification.objects.create(user=accept_task.user, description=f"Ваша заявка на подтверждение {accept_task.task.id} задания была утверждена!")

        accept_task.confirmed = True
        accept_task.doer = request.user
        accept_task.save()

        profile = Profile.objects.get(user=accept_task.user)
        interest_field = f"{accept_task.task.interest.lower()}_rating"  # Например, "food_rating"

        # Получаем текущее значение рейтинга
        current_rating = getattr(profile, interest_field, None)

        if current_rating is not None:
            # Обновляем значение рейтинга в зависимости от сложности задания
            if accept_task.task.difficulty == "easy":
                setattr(profile, interest_field, current_rating + 4)
            elif accept_task.task.difficulty == "medium":
                setattr(profile, interest_field, current_rating + 20)
            elif accept_task.task.difficulty == "hard":
                setattr(profile, interest_field, current_rating + 100)
            
            # Сохраняем изменения в профиле
            profile.save()

        return HttpResponse(status=200)



