from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import Calendar
from ..serializers import Calendar_Serializer
from rest_framework import status


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


    def post():
        pass
    def put():
        pass

    def delete():
        pass
    def patch(self, request, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        pending_hosts = request.data.get('pending_hosts')
        pending_guests = request.data.get('pending_guests')
        
        if pending_hosts is not None:
            calendar.pending_hosts = pending_hosts
        
        if pending_guests is not None:
            calendar.pending_guests = pending_guests
        
        calendar.save()
        
        return Response(status=status.HTTP_200_OK)
        


'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_all(request):
    """
    allows a user to view all the calendars they own, moderate, or subscribe to
    """
    owned_calendars = Calendar.objects.filter(owner=request.user)
    moderated_calendars = Calendar.objects.filter(hosts=request.user)
    subscribed_calendars = Calendar.objects.filter(guests=request.user)

    total_calendars = owned_calendars | moderated_calendars | subscribed_calendars
    serializer = Calendar_Serializer(total_calendars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_calendar(request, calendar_id):
    """
    allows a user to view a specific calendar given the calendar id
    """
    owned_calendars = Calendar.objects.filter(owner=request.user)
    moderated_calendars =  Calendar.objects.filter(hosts=request.user) 
    subscribed_calendars =  Calendar.objects.filter(guests=request.user)
    all_calendars = owned_calendars | moderated_calendars | subscribed_calendars
    
    try:
        # case 1. calendar exists
        calendar = all_calendars.get(id=calendar_id)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    # case 2. calendar does not exist
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_calendar(request):
    """
    allows the user to create a new calendar with optional 
    arguments such as a guest list, a host list, and a description
    """
    serializer = CalendarSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # what are all the possible errors that can occur?
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


@api_view(['DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def delete_calendar(request, calendar_id):
    """
    allows the user to delete a calendar given the calendar id
    """
    try:
        # case 1. the calendar exists, the user is the owner, and there are no hosts
        calendar = Calendar.objects.get(id=calendar_id)
        if calendar.owner == request.user and calendar.hosts.count() == 0:
            calendar.delete()
            return Response({"success": "The calendar has been deleted successfully"}, status=status.HTTP_200_OK)
        
        # case 2. the calendar exists, the user is the owner, and there are hosts
        elif calendar.owner == request.user and calendar.hosts.count() > 0:
            hosts = calendar.hosts.all()
            calendar.owner = hosts[0]
            calendar.save()
            return Response({"success": "The calendar has been deleted successfully"}, status=status.HTTP_200_OK)
        
        # case 3. the calendar exists but the user is not the owner
        else:
            return Response({"error": "Unauthorized action"}, status=status.HTTP_403_FORBIDDEN)
        
    # case 4. the calendar does not exist
    except Calendar.DoesNotExist:
        return Response({'error': "Invalid Calendar"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_owner(request, calendar_id):
    """
    allows the user to change the owner of a calendar and become a general host
    """
    # executes when the calendar exists
    try:
        calendar = Calendar.objects.get(id=calendar_id)

        # verification
        # check if the user is not the owner
        if calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        new_owner = request.data.get('new_owner')
        if new_owner == None:
            return Response({'error': 'No owner provided'}, status=status.HTTP_400_BAD_REQUEST)

        # check if the new owner is not a host
        if new_owner not in calendar.hosts.all():
            return Response({'error': "Invalid host"}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.owner = new_owner
        calendar.save()
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
            
    
    # executes when the calendar does not exist   
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)

     

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_host(request, calendar_id):
    """
    allows the user and other calendar hosts to add a new host to the calendar
    """
    # check if the calendar exists
    try:
        calendar = Calendar.objects.get(id=calendar_id)
        
        # check if the user is a host or the owner
        hosts = calendar.hosts.all()
        if request.user not in hosts and calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        new_host = request.data.get('new_host')
        if new_host == None:
            return Response({'error': 'No host provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the new host is not already a host
        if new_host in hosts:
            return Response({'error': 'Host already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.hosts.add(new_host)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_guest(request, calendar_id):
    """
    allows users and hosts to invite guests to a calendar
    """
    try:
        calendar = Calendar.objects.get(id=calendar_id)
        hosts = calendar.hosts.all()
        guests = calendar.guests.all()
        
        # check if the user is a host or the owner
        if request.user not in hosts and calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        new_guest = request.data.get('new_guest')
        if new_guest == None:
            return Response({'error': 'No guest provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the new guest is not already a guest
        if new_guest in guests:
            return Response({'error': 'Guest already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.guests.add(new_guest)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_guest(request, calendar_id):
    """
    allows users and hosts to remove guests from a calendar
    """
    try:
        calendar = Calendar.objects.get(id=calendar_id)
        hosts = calendar.hosts.all()
        guests = calendar.guests.all()
        
        # check if the user is a host or the owner
        if request.user not in hosts and calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        guest = request.data.get('guest')
        if guest == None:
            return Response({'error': 'No guest provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the guest exists
        if guest not in guests:
            return Response({'error': 'Guest does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.guests.remove(guest)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_host(request, calendar_id):
    """
    allows only the owner to remove hosts from a calendar
    """
    try:
        calendar = Calendar.objects.get(id=calendar_id)
        
        # check if the user is the owner
        if calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        host = request.data.get('host')
        if host == None:
            return Response({'error': 'No host provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the host exists
        if host not in calendar.hosts.all():
            return Response({'error': 'Host does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.hosts.remove(host)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_description(request, calendar_id):
    """
    allows the owner or hosts to update the description of a calendar
    """
    try:
        calendar = Calendar.objects.get(id=calendar_id)
        hosts = calendar.hosts.all()
        
        # check if the user is a host or the owner
        if request.user not in hosts and calendar.owner != request.user:
            return Response({'error': 'Unauthorized action'}, status=status.HTTP_403_FORBIDDEN)
        
        # check if the request is valid
        description = request.data.get('description')
        if description == None:
            return Response({'error': 'No description provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar.description = description
        calendar.save()
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    except Calendar.DoesNotExist:
        return Response({'error': 'Invalid Calendar'}, status=status.HTTP_404_NOT_FOUND)
    
### add functionality to change total availability of a calendar. 
### how to handle events when a new host is added?
'''