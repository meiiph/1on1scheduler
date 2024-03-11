from rest_framework import serializers
from .models import Calendar

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'owner', 'hosts', 'guests', 'start_date', 'end_date', 'description', 'pending_hosts', 'pending_guests']
