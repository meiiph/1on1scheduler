from rest_framework import serializers
from .models import Availability
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from calendars.models import Calendar
from calendars.serializers import CalendarSerializer
from django.utils import timezone

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['calendar', 'start', 'end', 'user']

    def validate_user(self, value):
        user = value
        calendar = get_object_or_404(Calendar, id=self.initial_data.get('calendar'))
        hosts = calendar.hosts.all()
        guests = calendar.guests.all()

        if user in hosts or user in guests or user == calendar.owner:
            return value
        else:
            raise serializers.ValidationError("you don't have access to this calendar")
        
    def validate_start(self, value):
        calendar = get_object_or_404(Calendar, id=self.initial_data.get('calendar'))
        if value < calendar.start_date:
            raise serializers.ValidationError("start time cannot be before calendar creation")
        return value

    def validate_end(self, value):
        start_time = self.initial_data.get('start')
        start = timezone.make_aware(timezone.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
        if value <= start:
            raise serializers.ValidationError("end time must be after start time")
        return value
    
    def to_representation(self, instance):
        response = {
                "start": instance.start,
                "end": instance.end
        }
        
        return response
        
            