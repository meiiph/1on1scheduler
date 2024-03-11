from rest_framework import serializers
from .models import Calendar, Event

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'user', 'name']  

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'organizer', 'attendees']