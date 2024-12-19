from notification.models import Notification

def notification_read(request):
    return Notification.read(request)
