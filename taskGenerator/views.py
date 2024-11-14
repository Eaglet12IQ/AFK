from django.shortcuts import render
from django.http import JsonResponse
import json
from taskGenerator.models import Tasks
import random
from typing import Dict, Union

def idea_generation(request):
    interests = json.loads(request.GET.get('interests'))
    difficulty = json.loads(request.GET.get('difficulty'))
    last_generations = json.loads(request.GET.get('last_generations'))

    last_generations_id_list = [gen['task_id'] for gen in last_generations]

    if not interests and not difficulty:
        tasks = Tasks.objects.filter().exclude(id__in=last_generations_id_list)
    elif not interests:
        tasks = Tasks.objects.filter(difficulty__in=difficulty).exclude(id__in=last_generations_id_list)
    elif not difficulty:
        tasks = Tasks.objects.filter(interest__in=interests).exclude(id__in=last_generations_id_list)
    else:
        tasks = Tasks.objects.filter(difficulty__in=difficulty, interest__in=interests).exclude(id__in=last_generations_id_list)

    random_task = random.choice(tasks)

    completed_task: Dict[str, Union[int, str]] = {
        "task_id": random_task.id,
        "task_description": random_task.description    
    }

    return JsonResponse(completed_task, status=200)
