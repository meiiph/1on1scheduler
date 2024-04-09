from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from calendars.models import Calendar
from .serializers import AvailabilitySerializer
from .models import Availability

@api_view(['POST'])
def create_availability(request, calendar_id):
    """
    handles the request object data
    
    {
    start
    end
    }
    
    sent to the endpoint availability/create/<calendar_id>. 
    creates an availability block or extends current availability blocks. 
    """
    user = request.user
    start = request.data.get('start')
    end = request.data.get('end')

    data = {
        "user": user.id,
        "start": start,
        "end": end,
        "calendar": calendar_id
    }

    serializer = AvailabilitySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


############# NOTES #########################
# need to make sure that adding the same availability isnt possible. 
# if an over lapping availability is added, it must be condesed into a single block. 
##############################################

@api_view(['DELETE'])
def remove_availability(request, calendar_id):
    """
    handles the request data object 
    
    {
    start
    end
    }
    
    sent to the endpoint availablity/remove/<calendar_id>.
    remove any potential availability from start to end. 
    """
    user = request.user
    calendar = get_object_or_404(Calendar, id=calendar_id)

    start = request.data.get('start')
    end = request.data.get('end')

    start = timezone.make_aware(timezone.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%fZ'))
    end = timezone.make_aware(timezone.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%fZ'))

    availabilities = Availability.objects.filter(user=user, calendar=calendar)
    for availability in availabilities:
        
        if availability.start < start < availability.end:
            if availability.start < end < availability.end:
                # case 1. availability contains start and end.
                Availability.objects.create(user=user, calendar=calendar, start=availability.start, end=start)
                Availability.objects.create(user=user, calendar=calendar, start=end, end=availability.end)
                availability.delete()

            else:
                # case 2. availability contains start only. 
                availability.end = start
                availability.save()

        elif availability.start < end < availability.end:
            # case 3. availability contains end only. 
            availability.start = end
            availability.save()
        
        # case 4. start and end contain availability. 
        elif start <= availability.start and end >= availability.end:
            availability.delete()

    return Response({"message": "availability has been modified"}, status=200)


@api_view(['GET'])
def view_availability(request, calendar_id):
    """
    handles the request data object 
    
    {
    
    }
    
    sent to the endpoint availability/view/<calendar_id>.
    gets the current user's total availablity for the calendar. 
    """
    user = request.user
    calendar = get_object_or_404(Calendar, id=calendar_id)
    hosts = calendar.hosts.all()
    guests = calendar.guests.all()

    if user in hosts or user in guests or user == calendar.owner:
        availabilities = Availability.objects.filter(calendar=calendar, user=user)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data, status=200)

    else:
        return Response({"error": "you dont not have access to this calendar."}, status=403)

############# NOTES #########################
# works well doesnt need to be improved much. 
##############################################