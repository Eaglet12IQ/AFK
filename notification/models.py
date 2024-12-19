from django.db import models
from authentication.models import User
import json
from django.http import HttpResponse, JsonResponse

class Notification(models.Model):
    description = models.TextField(max_length=100)
    sent_when = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def notifications_delete(request):
        data = json.loads(request.body)
        delete_id = data.get('delete_id')

        Notification.objects.get(id=delete_id).delete()

        return HttpResponse(status=200)
    
    def notifications_edit(request):
        data = json.loads(request.body)
        edit_id = data.get('edit_id')
        description = data.get('description')

        notification = Notification.objects.get(id=edit_id)
        notification.description = description
        notification.save()

        return JsonResponse({"message": "Данные уведомления изменены."}, status=200)
    
    def notifications_add(request):
        data = json.loads(request.body)
        id_user = data.get('id_user')
        description = data.get('description')

        if id_user == "all":
            users = User.objects.all()
        else:
            try:
                user_ids = [int(user_id.strip()) for user_id in id_user.split(',')]
            except ValueError as e:
                return JsonResponse({"message": "Неверный ввод."}, status=400)
            users = User.objects.filter(id__in=user_ids)
            if not users:
                return JsonResponse({"message": "Пользователя с таким ID не существует."}, status=400)
        

        notifications = [
                Notification(description=description, user=user) for user in users
            ]
        Notification.objects.bulk_create(notifications)
        
        return JsonResponse({"message": "Уведомление создано."}, status=201)
    
    def read(request):
        data = json.loads(request.body)
        id = data.get('id')

        notification = Notification.objects.get(id=id)

        notification.checked = True
        notification.save()
        
        return JsonResponse({"message": "Уведомление прочитано."}, status=200)