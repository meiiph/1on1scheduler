from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hosts = models.ManyToManyField(User, related_name='host_calendars', blank=True)
    guests = models.ManyToManyField(User, related_name='guest_calendars', blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)