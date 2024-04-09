from rest_framework import serializers
from .models import Invitation
from django.shortcuts import get_object_or_404
from calendars.models import Calendar
from django.contrib.auth.models import User

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['sender', 'receiver', 'calendar', 'invitation_type']

    def validate_invitation_type(self, value):
        valid_types = dict(Invitation.INVITATION_TYPES)
        if value not in valid_types:
            raise serializers.ValidationError("invalid invitation type")
        return value
    
    def validate_sender(self, value):
        calendar_id = self.initial_data.get('calendar')
        sender_id = self.initial_data.get('sender')

        calendar = get_object_or_404(Calendar, id=calendar_id)
        sender = get_object_or_404(User, id=sender_id)

        if calendar.owner == sender or sender in calendar.hosts.all():
            return value
        else:
            raise serializers.ValidationError("you do not have invite permissions")
        
    def validate_receiver(self, value):
        calendar_id = self.initial_data.get('calendar')
        receiver_id = self.initial_data.get('receiver')
        calendar = get_object_or_404(Calendar, id=calendar_id)
        receiver = get_object_or_404(User, id=receiver_id)
        if receiver == calendar.owner or receiver in calendar.guests.all() or receiver in calendar.hosts.all():
            raise serializers.ValidationError("the receiver already belongs to this calendar")
        return value

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'sender_username': instance.sender.username,
            'receiver_username': instance.receiver.username,
            'calendar_id': instance.calendar.id,
            'invitation_type': instance.invitation_type
        }
        return data