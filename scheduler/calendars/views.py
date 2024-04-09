from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .serializers import CalendarSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
from .models import Calendar
from django.contrib.auth.models import User

@api_view(['POST'])
def create(request):
    """
    handles the request object data

    {
    name
    description [optional]
    start_date [optional]
    end_date [optional]
    } 

    sent to the endpoint calendars/create.
    """ 
    user = request.user
    start_date = timezone.now().isoformat()

    data = {
    
    'name': request.data.get('name'),
    'description': request.data.get('description', ""),
    'start_date': request.data.get('start_date', start_date),
    'end_date': request.data.get('end_date', None),
    'owner': user.id

    }


    serializer = CalendarSerializer(data=data, context={'current_user': user})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_all(request):
    """
    handles the request object data

    {
    type [optional] valid values are: 'own', 'host', 'super_host', 'guest'
    }
    
    sent to the endpoint calendars/all
    retrieves calendars that a user owns, hosts, or is a guest of
    if request.query_params is empty all types are returned. 
    """
    user = request.user
    permission_type = request.query_params.get('type')

    if not permission_type:
        calendars = (Calendar.objects.filter(owner=user) |
                    Calendar.objects.filter(hosts=user) |
                    Calendar.objects.filter(guests=user))
        
    elif permission_type == 'own':
        calendars = Calendar.objects.filter(owner=user)

    elif permission_type == 'host':
        calendars = Calendar.objects.filter(hosts=user)

    elif permission_type == 'guest':
        calendars = Calendar.objects.filter(guests=user)

    else:
        return Response({'error': 'invalid type parameter'}, status=400)
    
    serializer = CalendarSerializer(calendars, many=True, context={'current_user': user})
    return Response(serializer.data, status=200)


@api_view(['GET'])
def view_one(request, id):
        """
        handles the request object data 

        {
        
        }

        sent to the endpoint calendars/<id>. 
        retrieves the calendar with the given id if it belongs to the current user,
        else return a 400 error. 
        """
        user = request.user
        calendar = get_object_or_404(Calendar, id=id)
        serializer = CalendarSerializer(calendar, context={'current_user': user})
        return Response(serializer.data, status=200)


@api_view(['DELETE'])       
def delete(request, id):
    """
    handles the request object data

    {
    
    }
    
    sent to the endpoint calendars/<id>/delete.
    deletes a calendar if the current user is the owner,
    else raises a 401 error.
    """
    user = request.user
    calendar = get_object_or_404(Calendar, id=id)
    if user == calendar.owner:
        calendar.delete()
        return Response({'message': 'calendar deleted successfully'}, status=200)
    else:
        return Response({'error': 'you do not have permission to delete the calendar'}, status=401)
    

@api_view(['PATCH'])       
def update_owner(request, id):
    """
    handles the request object data 
    
    {
    new_owner
    }

    sent to the endpoint <int:id>/update/owner
    """
    user = request.user
    calendar = get_object_or_404(Calendar, id=id)
    new_owner = request.data.get('new_owner')
    other_user = get_object_or_404(User, username=new_owner)

    if user != calendar.owner:
        return Response({'error': 'you do not have permission to update the owner'}, status=401)
    
    elif other_user not in calendar.hosts.all() and other_user not in calendar.guests.all():
        return Response({'error': 'invalid request'}, status=401)
    
    else:
        calendar.hosts.add(calendar.owner)
        calendar.owner = other_user
        calendar.hosts.remove(other_user)
        calendar.save()
        return Response({'message': 'owner updated successfully'}, status=200)


@api_view(['PATCH'])
def remove_user(request, id):
    """
    handles the request 
    
    {
    username
    }
    
    sent to the endpoint <int:id>/remove/user
    """
    owner = request.user
    other = get_object_or_404(User, username=request.data.get('username'))

    calendar = get_object_or_404(Calendar, id=id)
    if owner != calendar.owner:
        return Response({'error': 'you do not have permission to remove a user'}, status=401)

    elif other not in calendar.hosts.all() and other not in calendar.guests.all():
        return Response({'error': 'invalid request'}, status=400)
    
    else:
        if other in calendar.hosts.all():
            calendar.hosts.remove(other)
        elif other in calendar.guests.all():
            calendar.guests.remove(other)
        return Response({'message': 'user removed successfully'}, status=200)
