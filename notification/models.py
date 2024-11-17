from django.db import models
from authentication.models import User

class Notification(models.Model):
    description = models.TextField(max_length=100)
    sent_when = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)