from django.db import models
from django.contrib.auth.models import User

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    busy_times = models.TextField() 
