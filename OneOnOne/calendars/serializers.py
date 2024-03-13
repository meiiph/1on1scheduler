from rest_framework import serializers
from rest_framework.serializers import DateTimeField
from .models import Calendar, Invitation, Event
from django.contrib.auth.models import User

class Moderator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

class Guest_Serializer(Moderator_Serializer):
    class Meta:
        fields = ['id', 'owner', 'hosts', 'description', 'name']

class Calendar_Serializer(serializers.Serializer):
    def to_representation(self, instance):
        user = self.context['request'].user
        if user in instance.guests.all():
            serializer = Guest_Serializer(instance)
        else: 
            serializer = Moderator_Serializer(instance)
        return serializer.data
    
class Create_Calendar_Serializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=300, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    pending_hosts = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    pending_guests = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, many=True)

    def validate(self, data):
        owner = data.get('owner')
        pending_hosts = data.get('pending_hosts', [])
        pending_guests = data.get('pending_guests', [])

        if not User.objects.filter(pk=owner.pk).exists():
            raise serializers.ValidationError("Owner does not exist.")
        
        for host in pending_hosts:
            if not User.objects.filter(pk=host.pk).exists():
                raise serializers.ValidationError("Pending host with ID {} does not exist.".format(host.pk))
            
        for guest in pending_guests:
            if not User.objects.filter(pk=guest.pk).exists():
                raise serializers.ValidationError("Pending guest with ID {} does not exist.".format(guest.pk))

        return data

    def create(self, validated_data):
        return Calendar.objects.create(**validated_data)


class ReceivedInvitationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True,
    )
    recipient = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True,
    )
    calendar = serializers.SlugRelatedField(
        slug_field='name',
        read_only = True,
    )

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'calendar', 'meeting_datetime', 'is_accepted']
        read_only_fields = ['id', 'sender', 'recipient', 'calendar', 'meeting_datetime']

class SentInvitationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True,
    )
    recipient = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    calendar = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Calendar.objects.all(),
    )

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'calendar', 'meeting_datetime', 'is_accepted']
        read_only_fields = ['id', 'sender', 'is_accepted']

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
