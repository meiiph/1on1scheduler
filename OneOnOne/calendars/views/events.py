from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ..models import Event, Calendar
from ..serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        calendar_name = request.data.get('calendar') 
        start_time = request.data.get('start_time')  
        duration_str = request.data.get('duration')

        duration_parts = [int(part) for part in duration_str.split(':')]
        duration = timedelta(hours=duration_parts[0], minutes=duration_parts[1], seconds=duration_parts[2])

        calendar = get_object_or_404(Calendar, name=calendar_name)  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=request.user, calendar=calendar, start_time=start_time, duration=duration)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EventAddAttendeeView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, pk=event_id)

    def patch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        instance = self.get_object()

        attendee = get_object_or_404(User, pk=user_id)

        instance.attendees.add(attendee)
        return Response(self.get_serializer(instance).data)

class EventRemoveAttendeeView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, pk=event_id)

    def patch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        instance = self.get_object()

        attendee = get_object_or_404(User, pk=user_id)

        if attendee in instance.attendees.all():
            instance.attendees.remove(attendee)
            return Response({'message': f'Attendee with ID {user_id} removed from event with ID {instance.id}'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': f'Attendee with ID {user_id} is not registered for event with ID {instance.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
class EventCancelView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventRequestJoinView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, pk=event_id)

    def patch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        instance = self.get_object()
        attendee = get_object_or_404(User, pk=user_id)
        instance.attendees.add(attendee)
        return Response(self.get_serializer(instance).data)
    
class UserEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)
