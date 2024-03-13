from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Contact(models.Model):
    curr_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curr_user')
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_user', verbose_name="username")
    name = models.CharField(max_length=100)
    email = models.EmailField()