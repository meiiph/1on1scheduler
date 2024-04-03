from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import Calendar
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Calendar_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        allows a user to get calendars that they own, host, or subscribe to as a guest. 
        if a list of calendar ids are provided as query parameters, view selected only. 
        """
        user = request.user 
        data = request.data
        
        calendar_names = data.get('calendar_names', [])

        owned_calendars = Calendar.objects.filter(owner=user)
        host_calendars = Calendar.objects.filter(pending_hosts=user)
        guest_calendars = Calendar.objects.filter(pending_guests=user)

        calendars = owned_calendars | host_calendars | guest_calendars
        
        response_data = []
        for calendar in calendars:
            calendar_data = {
                "name": calendar.name,
                "description": calendar.description,
                "owner": calendar.owner.username
            }
            response_data.append(calendar_data)
        
        return Response(response_data, status=status.HTTP_200_OK)

    
    def post(self, request):
        """
        allows a user to create a calendar. they must specify the name of the calendar but can add an optional
        description, pending hosts, and pending guests
        """
        user = request.user
        data = request.data 
        name = data.get('name')
        description = data.get('description', '')
        pending_hosts = data.get('pending_hosts', [])
        pending_guests = data.get('pending_guests', [])

        calendar = Calendar.objects.create(
            name=name,
            description=description,
            owner=user
        )

        for username in pending_hosts:
            try:
                p_host = User.objects.get(username=username)
                calendar.pending_hosts.add(p_host)
            except User.DoesNotExist:
                return Response({"error": "at least one pending host in invalid"}, status=status.HTTP_400_BAD_REQUEST)

        for username in pending_guests:
            try:
                p_guest = User.objects.get(username=username)
                calendar.pending_guests.add(p_guest)
            except User.DoesNotExist:
                return Response({"error": "at least one pending guest in invalid"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "name": calendar.name,
            "owner_username": calendar.owner.username,
            "pending_hosts": [user.username for user in calendar.pending_hosts.all()],
            "pending_guests": [user.username for user in calendar.pending_guests.all()]
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    

    def delete(self, request):
        calendar_name = request.data.get('name')
        
        if not calendar_name:
            return Response({"error": "Calendar name not provided in request body."},
                            status=status.HTTP_400_BAD_REQUEST)


        calendar = get_object_or_404(Calendar, name=calendar_name)
        
        if request.user != calendar.owner:
            return Response({"error": "You are not authorized to delete this calendar."},
                            status=status.HTTP_403_FORBIDDEN)


        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 