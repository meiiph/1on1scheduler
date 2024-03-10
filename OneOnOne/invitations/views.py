from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Invitation
from .serializers import InvitationSerializer
# from .models import User

class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(invitee=self.request.user)
    
    def get(self, serializer):
        invitations = Invitation.objects.filter(invitee=self.request.user)
        serializer = InvitationSerializer(invitations, many=True)
        # serializer.save(receiver=self.request.user)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

class InvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvitationSerializer 

    def get(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        # invitation = get_object_or_404(Invitation, pk=invitation_id)

        serializer = InvitationSerializer(invitation)
        return JsonResponse(serializer.data)
    
    def put(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        serializer = InvitationSerializer(invitation, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        invitation.delete()
        return HttpResponse('NO CONTENT', status=204)