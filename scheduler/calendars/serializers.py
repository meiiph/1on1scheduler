from rest_framework import serializers
from .models import Calendar
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from accounts.serializers import UserSerializer
from datetime import timedelta

class CalendarSerializer(serializers.ModelSerializer):
    """
    a serializer for the calendar model. 
    """
    class Meta:
        model = Calendar
        fields = ['name', 'description', 'start_date', 'end_date', 'owner']

    def validate_name(self, value):
        """
        validates the calendar's name. it must have between 4 to 100 characters.
        """
        if len(value) < 4:
            raise serializers.ValidationError("name must have at least 4 characters.")
        
        elif len(value) > 100:
            raise serializers.ValidationError("name must have at most 100 characters.")
        
        else:
            return value
        
    def validate_description(self, value):
        """
        validates the description field to ensure it is less than or equal to 200 characters.
        """
        if len(value) > 200:
            raise serializers.ValidationError("description must be less than or equal to 200 characters.")
        return value
    
    def validate_end_date(self, value):
        """
        validates end_date. ensures that the end_date is after the start date or its None. 
        """
        start_date = self.initial_data.get('start_date')
        if start_date < start_date:
            raise serializers.ValidationError("end date must be after the start date.")
        return value
    
    def validate_start_date(self, value):
        """
        validates the start date. checks that the start date of the calendar is no more than 10
        days ago.
        """
        if value.date() < timezone.now().date() - timedelta(days=10):
            raise serializers.ValidationError("start date must be more than 10 days ago.")
        return value
    

    def to_representation(self, instance):
        """
        returns a json representation of a calendar object. 
        """

        representation = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'end_date': instance.end_date,
            'start_date': instance.start_date,
            'owner': UserSerializer(instance.owner).data, 
            'hosts': UserSerializer(instance.hosts.all(), many=True).data,
        }
        current_user = self.context.get('current_user')
        priority_users = instance.hosts.all()

        if current_user in priority_users or current_user == instance.owner:
            representation['guests'] = UserSerializer(instance.guests.all(), many=True).data
            return representation
        elif current_user in instance.guests.all():
            return representation
        else:
            raise PermissionDenied("you do not have permission to view this calendar.")


        
        