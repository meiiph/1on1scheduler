from rest_framework import serializers
from rest_framework import serializers
from .models import Availability, Event


class AvailabilitySerailzier(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



    