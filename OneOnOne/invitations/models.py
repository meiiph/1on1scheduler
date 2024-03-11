# from django.contrib.auth.models import User
# from django.db import models
# from calendars.models import Calendar

# class Invitation(models.Model):
#     # inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
#     # invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
#     # meeting_datetime = models.DateTimeField()
#     # is_accepted = models.BooleanField(default=False)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
#     calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='invitations')
#     meeting_datetime = models.DateTimeField()
#     is_accepted = models.BooleanField(default=False, verbose_name="Accept Invitation")