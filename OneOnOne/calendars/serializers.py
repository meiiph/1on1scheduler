from rest_framework import serializers
from .models import Calendar, Invitation, Event
from django.contrib.auth.models import User


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'owner', 'hosts', 'guests', 'start_date', 'end_date', 'description', 'pending_hosts', 'pending_guests']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'calendar', 'meeting_datetime', 'is_accepted']

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    attendees = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.all(),
    )
    calendar = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Calendar.objects.all(),
    )

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'start_time', 'organizer', 'attendees', 'calendar', 'duration']
