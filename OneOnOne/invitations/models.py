from django.contrib.auth.models import User
from django.db import models

class Invitation(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    meeting_datetime = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)