from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Invitation
from .serializers import InvitationSerializer
from .models import User

class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(invitee=self.request.user)
    
    def get(self, serializer):
        invitations = Invitation.objects.filter(invitee=self.request.user)
        serializer = InvitationSerializer(invitations, many=True)
        # serializer.save(receiver=self.request.user)
        serializer_data = serializer.data
        for i in range(len(serializer.data)):
            serializer_data[i]['inviter'] = User.objects.get(id=serializer_data[i]['inviter']).username
            serializer_data[i]['invitee'] = User.objects.get(id=serializer_data[i]['invitee']).username
        return JsonResponse(serializer_data, safe=False)
    
    def post(self, request):
        request.data['inviter'] = User.objects.get(username=request.data['inviter']).id
        request.data['invitee'] = User.objects.get(username=request.data['invitee']).id
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_data = serializer.data
            serializer_data['inviter'] = User.objects.get(id=serializer_data['inviter']).username
            serializer_data['invitee'] = User.objects.get(id=serializer_data['invitee']).username
            return JsonResponse(serializer_data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

class InvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvitationSerializer 

    def get(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        # invitation = get_object_or_404(Invitation, pk=invitation_id)

        serializer = InvitationSerializer(invitation)
        serializer_data = serializer.data
        serializer_data['inviter'] = User.objects.get(id=serializer_data['inviter']).username
        serializer_data['invitee'] = User.objects.get(id=serializer_data['invitee']).username

        return JsonResponse(serializer_data)
        # return JsonResponse(serializer.data)
    
    def put(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        self.request.data['inviter'] = User.objects.get(username=self.request.data['inviter']).id
        self.request.data['invitee'] = User.objects.get(username=self.request.data['invitee']).id
        serializer = InvitationSerializer(invitation, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            serializer_data = serializer.data
            serializer_data['inviter'] = User.objects.get(id=serializer_data['inviter']).username
            serializer_data['invitee'] = User.objects.get(id=serializer_data['invitee']).username
            return JsonResponse(serializer_data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        invitation.delete()
        return HttpResponse('NO CONTENT', status=204)