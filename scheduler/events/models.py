from django.db import models
from django.contrib.auth.models import User
from calendars.models import Calendar
from django.db import models
from django.contrib.auth.models import User
from calendars.models import Calendar

class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')
    invited_user = models.ManyToManyField(User, related_name='invited_events')
    valid_from = models.DateField()
    valid_to = models.DateField()
    start = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    confirmation_status = models.BooleanField(default=False)

class Availability(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)