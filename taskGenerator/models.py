from django.db import models

class Tasks(models.Model):
    description = models.TextField(max_length=100)
    difficulty = models.TextField(max_length=10)
    interest = models.TextField(max_length=30)
