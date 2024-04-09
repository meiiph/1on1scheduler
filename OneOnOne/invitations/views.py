from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import InvitationSerializer
from .models import Invitation
from django.contrib.auth.models import User
from calendars.models import Calendar
from django.core.mail import send_mail

@api_view(['POST'])
def send_invitation(request, calendar_id):
    """
    handles the request object data
    
    {
    username
    type
    }

    sent to the endpoint invitations/<int:calendar_id>/send.
    allows the current user to send an invitation to the user with username. 
    the type of invitation is required and its either guest, host, or super_host. 
    """
    receiver_username = request.data.get('username')
    receiver = get_object_or_404(User, username=receiver_username)
    calendar = get_object_or_404(Calendar, id=calendar_id)

    data = {
        'sender': request.user.id,
        'receiver': get_object_or_404(User, username=receiver_username).id,
        'calendar': get_object_or_404(Calendar, id=calendar_id).id,
        'invitation_type': request.data.get('type')
    }
    
    serializer = InvitationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        subject = 'You have received an invitation'
        message = f'You have received an invitation from {request.user.username} for calendar {calendar.name}. Invitation Type: {request.data.get('type')}'
        receiver_email = receiver.email
        send_mail(subject, message, 'norelpy@example.com', [receiver_email])

        return Response({'message': f'Invitation sent successfully to {receiver_username}'}, status=201)
    else:
        return Response(serializer.errors, status=400)
    


@api_view(['GET'])
def view_all(request):
    """
    handles the request object data

    {
    type [sent or received]
    }

    sent to the endpoint invitations/all. 
    allows the current user to view all the invitations they have sent or received. 
    """
    user = request.user
    invitation_type = request.data.get('type')
    if invitation_type == 'received':
        invitations = Invitation.objects.filter(receiver=user)
        serializer = InvitationSerializer(invitations, many=True)
        for invite in serializer.data:
            invite.pop('receiver_username')
        return Response(serializer.data, status=200)
    
    elif invitation_type == 'sent':
        invitations_sent = Invitation.objects.filter(sender=user)
        serializer = InvitationSerializer(invitations_sent, many=True)
        for invite in serializer.data:
            invite.pop('sender_username')
        return Response(serializer.data, status=200)
        
    else:
        return Response({'message': 'invalid request'}, status=400)


@api_view(['GET'])
def view_one(request, id):
    """
    handles the request object data

    {
    
    }

    sent to the endpoint invitations/<id>. 
    allows the current user to view invitation with the id, if they are authorized to. 
    """
    user = request.user
    invitation = get_object_or_404(Invitation, id=id)

    if invitation.receiver != user and invitation.sender != user:
        return Response({'message': 'you are not authorized to view this invitation'}, status=403)
    
    serializer = InvitationSerializer(invitation)
    return Response(serializer.data)


@api_view(['DELETE'])
def respond(request, invitation_id):
    """
    handles the request object data
    
    {
    status[must be accept or decline]
    }

    sent to the endpoint invitations/<invitation_id>/respond.
    allows the current user to accept or decline an invitation.
    this will add the user to the calendar if the user accepts. 
    """
    user = request.user
    status = request.data.get('status')
    invitation = get_object_or_404(Invitation, id=invitation_id)

    if invitation.receiver != user:
            return Response({'message': 'you are not authorized to accept this invitation'}, status=403)

    if status == 'accept':
        calendar = invitation.calendar
        invitation_type = invitation.invitation_type
        
        if invitation_type == 'guest':
            calendar.guests.add(user)
        
        elif invitation_type == 'host':
            calendar.hosts.add(user)

        invitation.delete()
        return Response({'message': f'you are now a {invitation_type} of calendar {calendar.name}'}, status=204)
    
    elif status == 'decline':
            invitation.delete()
            return Response({'message': 'invitation declined successfully'}, status=204)
    else:
        return Response({'message': 'invalid request'}, status=400)


@api_view(['DELETE'])
def delete_invitation(request, invitation_id):
    """
    handles the request object data 

    {
    
    }

    sent to the endpoint invitations/<inviation_id>/delete. 
    deletes an invitation. 
    """
    user = request.user
    invitation = get_object_or_404(Invitation, id=invitation_id)

    if user == invitation.sender or user == invitation.receiver:
        invitation.delete()
        return Response({'message': 'invitation deleted successfully'}, status=204)
    else:
        return Response({'error': 'you do not have permission to delete this invitation'}, status=403)

