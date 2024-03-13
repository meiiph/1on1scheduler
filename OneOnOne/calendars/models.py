from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_calendars')
    hosts = models.ManyToManyField(User, related_name='moderated_calendars')
    guests = models.ManyToManyField(User, related_name='subscribed_calendars')
    description = models.TextField()
    pending_hosts = models.ManyToManyField(User, related_name='pending_moderator_calendars')
    pending_guests = models.ManyToManyField(User, related_name='pending_subscriber_calendars')


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    start_time = models.TimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events_attending')
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    duration = models.DurationField()

class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='invitations_received')
    meeting_datetime = models.DateTimeField()
    is_accepted = models.BooleanField(default=False, verbose_name="Accept Invitation")
