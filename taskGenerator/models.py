from django.db import models
from django.http import JsonResponse
import json
import random
from typing import Dict, Union
from authentication.models import User

class Tasks(models.Model):
    description = models.TextField(max_length=100)
    difficulty = models.TextField(max_length=10)
    interest = models.TextField(max_length=30)

    def idea_generation(request):
        interests = json.loads(request.GET.get('interests'))
        difficulty = json.loads(request.GET.get('difficulty'))

        from taskGenerator.models import completedTask
        last_generations_id_list = [gen.task.id for gen in completedTask.objects.filter(user=request.user).order_by('-id')[:10]]

        if not interests and not difficulty:
            tasks = Tasks.objects.filter().exclude(id__in=last_generations_id_list)
        elif not interests:
            tasks = Tasks.objects.filter(difficulty__in=difficulty).exclude(id__in=last_generations_id_list)
        elif not difficulty:
            tasks = Tasks.objects.filter(interest__in=interests).exclude(id__in=last_generations_id_list)
        else:
            tasks = Tasks.objects.filter(difficulty__in=difficulty, interest__in=interests).exclude(id__in=last_generations_id_list)

        random_task = random.choice(tasks)

        completedTask.objects.create(task=random_task, user=request.user, confirmed=False)

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
    confirmed = models.BooleanField()
