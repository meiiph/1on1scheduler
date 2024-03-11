from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    time = models.TimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events_attending')