from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import Calendar
from ..serializers import Calendar_Serializer, Create_Calendar_Serializer
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
        serializer = Calendar_Serializer 
        user = request.user 
        calendar_ids = request.query_params.getlist('calendar_ids')

        if calendar_ids is None:
            owned_calendars = Calendar.objects.filter(owner=user)
            host_calendars = Calendar.objects.filter(hosts=user)
            guest_calendars = Calendar.objects.filter(guests=user)

            total = owned_calendars | host_calendars | guest_calendars
            serializer = Calendar_Serializer(total, many=True, context={'request': request})

            return Response(serializer.data)
        # if the user specifies a list of calendars
        else :
            calendars = Calendar.objects.filter(id__in=calendar_ids)
            serializer = Calendar_Serializer(calendars, many=True, context={'request': request})
            return Response(serializer.data)


    def post(self, request):
        """
        allows a user to create a calendar. they must specify the name of the calendar but can add an optional
        description, pending hosts, and pending guests
        """            
        serializer = Create_Calendar_Serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, calendar_id):
        calendar = get_object_or_404(Calendar, id=calendar_id)
        
        if request.user != calendar.owner:
            return Response({"error": "You are not authorized to delete this calendar."},
                            status=status.HTTP_403_FORBIDDEN)

        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def patch(self, request, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        pending_hosts = request.data.get('pending_hosts')
        pending_guests = request.data.get('pending_guests')
        
        for host_id in pending_hosts:
            if not User.objects.filter(pk=host_id).exists():
                return Response({"error": f"Invalid pending host ID: {host_id}"}, status=status.HTTP_400_BAD_REQUEST)

        calendar.pending_hosts = pending_hosts
        calendar.pending_guests = pending_guests
        calendar.save()
        
        return Response(status=status.HTTP_200_OK)
        

