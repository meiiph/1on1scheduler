from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_calendars')
    hosts = models.ManyToManyField(User, related_name='moderated_calendars')
    guests = models.ManyToManyField(User, related_name='subscribed_calendars')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    pending_hosts = models.ManyToManyField(User, related_name='pending_moderator_calendars')
    pending_guests = models.ManyToManyField(User, related_name='pending_subscriber_calendars')


class Event(models.Model):
    EVENT_TYPES = [
        ('OPEN', 'Open'),
        ('REGISTRATION_REQUIRED', 'Registration Required'),
    ]
    RECCURANCES = [
        ('NEVER', 'Never'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    recurrence = models.CharField(max_length=100, choices=RECCURANCES)
    attending_guests = models.ManyToManyField(User, related_name='attending_events')
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES)
    attendee_limit = models.PositiveIntegerField(null=True, blank=True)

class Invitation(models.Model):
    INVITATION_TYPES = [
        ('MODERATOR', 'Moderator'),
        ('SUBSCRIBER', 'Subscriber'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=100, choices=INVITATION_TYPES)
