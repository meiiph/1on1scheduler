from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'inviter', 'invitee', 'meeting_datetime'] 
