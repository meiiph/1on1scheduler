from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class Signup_View(APIView): 
    """
    this class defines the behavior of the /auth/signup endpoint
    this endpoint will only support get and post requests
    the endpoint is used to create a new user
    Signup_Serializer is used to validate the data sent to the endpoint and create a new user
    """
    serializer_class = serializers.Signup_Serializer
    permission_classes = [AllowAny]

    def get(self, request):
        """
        this method is called when a GET request is sent to the /auth/signup endpoint
        """
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        this method is called when a POST request is sent to the /auth/signup endpoint
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "A new user has been created",
                             "username" : user.username,
                             "first_name" : user.first_name,
                             "last_name" : user.last_name}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class Logout_View(APIView):
    """
    this class defines the behavior of the /auth/logout endpoint
    the endpoint is used to log out a user
    this endpoint will only support post requests
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        this method is called when a POST request is sent to the /auth/logout endpoint
        """
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Success"}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)