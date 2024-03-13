from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(curr_user=self.request.user)
    
    def get(self, serializer):
        contacts = Contact.objects.filter(curr_user=self.request.user)
        serializer = ContactSerializer(contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(curr_user=self.request.user)
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        serializer = ContactSerializer(contact)
        return JsonResponse(serializer.data)
    
    def put(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        serializer = ContactSerializer(contact, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        contact.delete()
        return HttpResponse('NO CONTENT', status=204)