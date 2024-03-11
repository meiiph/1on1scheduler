from django.contrib import admin
from .models import Invitation, Event

admin.site.register(Invitation)

admin.site.register(Event)