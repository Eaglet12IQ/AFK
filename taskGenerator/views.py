from django.shortcuts import render
from django.http import JsonResponse
import json
from taskGenerator.models import Tasks
import random

def idea_generation(request):
    interests = json.loads(request.GET.get('interests'))
    difficulty = request.GET.get('difficulty')
    last_generations = json.loads(request.GET.get('last_generations'))

    last_generations_id_list = [key for gen in last_generations for key in gen.keys()]

    if not interests and difficulty is None:
        tasks = Tasks.objects.filter().exclude(id__in=last_generations_id_list)
    elif not interests:
        tasks = Tasks.objects.filter(difficulty=difficulty).exclude(id__in=last_generations_id_list)
    elif difficulty is None:
        tasks = Tasks.objects.filter(interest__in=interests).exclude(id__in=last_generations_id_list)
    else:
        tasks = Tasks.objects.filter(difficulty=difficulty, interest__in=interests).exclude(id__in=last_generations_id_list)

    random_task = random.choice(tasks)

    return JsonResponse({"completed_task": {f"{random_task.id}": random_task.description}}, status=200)
