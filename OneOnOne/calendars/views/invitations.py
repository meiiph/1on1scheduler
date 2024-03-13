from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from ..models import Invitation, User, Calendar
from ..serializers import InvitationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = InvitationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invitation.objects.filter(recipient=self.request.user)
    
    def get(self, serializer):
        invitations = Invitation.objects.filter(recipient=self.request.user)
        serializer = InvitationSerializer(invitations, many=True)
        # serializer.save(receiver=self.request.user)
        serializer_data = serializer.data
        for i in range(len(serializer.data)):
            serializer_data[i]['sender'] = User.objects.get(id=serializer_data[i]['sender']).username
            serializer_data[i]['recipient'] = User.objects.get(id=serializer_data[i]['recipient']).username
            serializer_data[i]['calendar'] = str(serializer_data[i]['calendar']) + ", " + Calendar.objects.get(id=serializer_data[i]['calendar']).name
        return JsonResponse(serializer_data, safe=False)
    
    def post(self, request):
        request.data['sender'] = User.objects.get(username=request.data['sender']).id
        request.data['recipient'] = User.objects.get(username=request.data['recipient']).id
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_data = serializer.data
            serializer_data['sender'] = User.objects.get(id=serializer_data['sender']).username
            serializer_data['recipient'] = User.objects.get(id=serializer_data['recipient']).username
            serializer_data['calendar'] = str(serializer_data['calendar']) + ", " + Calendar.objects.get(id=serializer_data['calendar']).name
            return JsonResponse(serializer_data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

class InvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvitationSerializer 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        # invitation = get_object_or_404(Invitation, pk=invitation_id)

        serializer = InvitationSerializer(invitation)
        serializer_data = serializer.data
        serializer_data['sender'] = User.objects.get(id=serializer_data['sender']).username
        serializer_data['recipient'] = User.objects.get(id=serializer_data['recipient']).username
        serializer_data['calendar'] = str(serializer_data['calendar']) + ", " + Calendar.objects.get(id=serializer_data['calendar']).name
        return JsonResponse(serializer_data)
        # return JsonResponse(serializer.data)
    
    def put(self, serializer, invitation_id):
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        self.request.data['sender'] = User.objects.get(username=self.request.data['sender']).id
        self.request.data['recipient'] = User.objects.get(username=self.request.data['recipient']).id
        serializer = InvitationSerializer(invitation, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            serializer_data = serializer.data
            serializer_data['sender'] = User.objects.get(id=serializer_data['sender']).username
            serializer_data['recipient'] = User.objects.get(id=serializer_data['recipient']).username
            serializer_data['calendar'] = str(serializer_data['calendar']) + ", " + Calendar.objects.get(id=serializer_data['calendar']).name
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