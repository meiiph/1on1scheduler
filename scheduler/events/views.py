from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import EventSerializer, AvailabilitySerailzier
from .models import Event

@api_view(['POST'])
def create(request, calendar_id):
    """
    creates a new event for the calendar. 

    {
    invited_username
    valid_from
    valid_to
    duration
    availability
    name
    description
    }
    """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save(calendar_id=calendar_id)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def view_event(request, calendar_id, event_id):
    """
    retrieves a single event from the calendar.
    """
    event = get_object_or_404(Event, calendar_id=calendar_id, id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def view_all_events(request, calendar_id):
    """
    retrieves all events from the calendar.
    """
    events = Event.objects.filter(calendar_id=calendar_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=200)


@api_view(['PUT'])
def confirm_event(request, calendar_id, event_id):
    """
    confirms an event by updating its availability blocks.
    {
    availability
    }
    """
    event = get_object_or_404(Event, calendar_id=calendar_id, id=event_id)
    serializer = AvailabilitySerailzier(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_event(request, calendar_id, event_id):
    """
    deletes an event from the calendar.
    """
    event = get_object_or_404(Event, calendar_id=calendar_id, id=event_id)
    event.delete()
    return Response(status=204)