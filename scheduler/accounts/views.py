from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone

class SignupView(APIView):
    """
    handles http requests sent to the endpoint accounts/signup
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        handles the following post request data:

        {
        [all required]
        username
        password 
        first_name 
        last_name
        email
        }
        
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


