from .models import Notification

def notifications_processor(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, checked=False)
    else:
        notifications = []
    
    return {
        'notifications': notifications
    }
