from rest_framework import serializers
from .models import Calendar, Invitation

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'owner', 'hosts', 'guests', 'start_date', 'end_date', 'description', 'pending_hosts', 'pending_guests']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'calendar', 'meeting_datetime', 'is_accepted']