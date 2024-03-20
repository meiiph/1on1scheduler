from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from ..models import Invitation, User, Calendar
from ..serializers import ReceivedInvitationSerializer, SentInvitationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ReceivedInvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReceivedInvitationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(recipient=self.request.user, is_accepted=False)
    
    def get(self, serializer):
        invitations = Invitation.objects.filter(recipient=self.request.user, is_accepted=False)
        serializer = ReceivedInvitationSerializer(invitations, many=True)
        return JsonResponse(serializer.data, safe=False)

class ReceivedInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReceivedInvitationSerializer 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, recipient=self.request.user, is_accepted=False)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        serializer = ReceivedInvitationSerializer(invitation)
        return JsonResponse(serializer.data)
    
    def put(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, recipient=self.request.user, is_accepted=False)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        serializer = ReceivedInvitationSerializer(invitation, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            # if serializer.data['is_accepted'] == True:
            #     invitation.delete()

            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, recipient=self.request.user, is_accepted=False)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        invitation.delete()
        return HttpResponse('NO CONTENT', status=204)


class SentInvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = SentInvitationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(sender=self.request.user)
    
    def get(self, serializer):
        invitations = Invitation.objects.filter(sender=self.request.user)
        serializer = SentInvitationSerializer(invitations, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        serializer = SentInvitationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                calendar = serializer.validated_data['calendar']
                if calendar.owner != self.request.user:
                    return HttpResponse('CALENDAR DOES NOT EXIST', status=400)
            except Calendar.DoesNotExist:
                return HttpResponse('CALENDAR DOES NOT EXIST', status=400)
            
            serializer.save(sender=self.request.user)
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

class SentInvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SentInvitationSerializer 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, sender=self.request.user)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        serializer = SentInvitationSerializer(invitation)
        return JsonResponse(serializer.data)
    
    def put(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, sender=self.request.user, is_accepted=False)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        serializer = SentInvitationSerializer(invitation, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id, sender=self.request.user)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        invitation.delete()
        return HttpResponse('NO CONTENT', status=204)