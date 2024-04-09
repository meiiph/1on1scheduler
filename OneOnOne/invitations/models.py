from django.db import models
from django.contrib.auth.models import User
from calendars.models import Calendar

class Invitation(models.Model):
    INVITATION_TYPES = [
        ('host', 'host'),
        ('guest', 'guest'),
        ('super_host', 'super_host'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    invitation_type = models.CharField(choices=INVITATION_TYPES, max_length=150)
    accepted = models.BooleanField(blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='invitations')
