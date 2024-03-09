from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)