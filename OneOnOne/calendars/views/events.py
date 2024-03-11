from rest_framework import generics
from ..models import Event
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from ..serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventAddAttendeeView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        attendee_id = request.data.get('attendee_id')
        attendee = get_object_or_404(User, pk=attendee_id)
        instance.attendees.add(attendee)
        return Response(self.get_serializer(instance).data)

class EventRemoveAttendeeView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        attendee_id = request.data.get('attendee_id')
        attendee = get_object_or_404(User, pk=attendee_id)
        instance.attendees.remove(attendee)
        return Response(self.get_serializer(instance).data)

class EventCancelView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

class EventRequestJoinView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        attendee_id = request.data.get('attendee_id')
        attendee = get_object_or_404(User, pk=attendee_id)
        instance.attendees.add(attendee)
        return Response(self.get_serializer(instance).data)
    
class UserEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)    