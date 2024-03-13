from django.contrib import admin
from .models import Invitation, Event, Calendar

admin.site.register(Invitation)

admin.site.register(Event)

admin.site.register(Calendar)