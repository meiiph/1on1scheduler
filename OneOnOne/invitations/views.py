from rest_framework import generics
from .models import Invitation
from .serializers import InvitationSerializer

class InvitationListCreateView(generics.ListCreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

class InvitationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer