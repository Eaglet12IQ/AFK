from django.shortcuts import render
from profiles.models import Profile
from taskGenerator.models import completedTask

def main_view(request):
    return render(request, "main.html", {'user': request.user})

def top_view(request):
    # Получаем всех пользователей, отсортированных по total_rating
    profiles = Profile.objects.order_by('-total_rating')

    # Добавляем количество завершенных задач и категорию с наибольшим рейтингом для каждого пользователя
    for profile in profiles:
        # Количество завершенных задач
        profile.completed_tasks_count = completedTask.objects.filter(user=profile.user.id).count()

        # Определяем категорию с наибольшим рейтингом
        category_ratings = {
            "Еда": profile.food_rating,
            "Спорт": profile.sport_rating,
            "Технологии": profile.technology_rating,
            "Путешествия": profile.travel_rating,
            "Искусство": profile.creative_rating,
        }
        # Находим категорию с наибольшим значением рейтинга
        profile.top_category = max(category_ratings, key=category_ratings.get)

    # Проверяем количество пользователей и безопасно выбираем топ-3
    top1 = profiles[0] if len(profiles) > 0 else None
    top2 = profiles[1] if len(profiles) > 1 else None
    top3 = profiles[2] if len(profiles) > 2 else None

    # Все остальные пользователи после топ-3
    other_users = profiles[3:] if len(profiles) > 3 else []

    # Лучшие профили для каждой категории
    best_food = Profile.objects.order_by('-food_rating').first()
    best_sport = Profile.objects.order_by('-sport_rating').first()
    best_technology = Profile.objects.order_by('-technology_rating').first()
    best_travel = Profile.objects.order_by('-travel_rating').first()
    best_creative = Profile.objects.order_by('-creative_rating').first()

    # Передаем данные в контекст
    context = {
        "top1": top1,
        "top2": top2,
        "top3": top3,
        "other_users": other_users,
        "best_food": best_food,
        "best_sport": best_sport,
        "best_technology": best_technology,
        "best_travel": best_travel,
        "best_creative": best_creative,
    }
    return render(request, "top.html", context)



