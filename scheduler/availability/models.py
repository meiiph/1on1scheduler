from django.db import models
from calendars.models import Calendar
from django.contrib.auth.models import User

class Availability(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)