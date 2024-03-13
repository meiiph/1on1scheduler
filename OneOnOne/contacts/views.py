from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from .models import Contact
from .models import User
from .serializers import ContactSerializer, UpdateContactSerializer
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

        try:
            user_id = User.objects.get(username=request.data['contact_user']).id  
        except User.DoesNotExist:
            return HttpResponse('BAD REQUEST: USER DOES NOT EXIST', status=400)
        
        if serializer.is_valid():
            try:
                user = User.objects.get(id=user_id) 
                potential_contact = Contact.objects.get(curr_user=self.request.user, contact_user=user)
                if potential_contact is not None:
                    return HttpResponse('BAD REQUEST: USER ALREADY IN CONTACTS', status=400)
            except Contact.DoesNotExist:
                # new_contact = Contact(curr_user=self.request.user, contact_user=user, name=request.data['name'], email=request.data['email'])
                # new_contact.save()
                serializer.save(curr_user=self.request.user)

            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id, curr_user=self.request.user)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)

        serializer = UpdateContactSerializer(contact)
        return JsonResponse(serializer.data)
    
    def put(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id, curr_user=self.request.user)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
    
        serializer = UpdateContactSerializer(contact, data=self.request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse('BAD REQUEST', status=400)

    def delete(self, serializer, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id, curr_user=self.request.user)
        except Contact.DoesNotExist:
            return HttpResponse('NOT FOUND', status=404)
        
        contact.delete()
        return HttpResponse('NO CONTENT', status=204)