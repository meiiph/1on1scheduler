from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class Signup_Serializer(serializers.Serializer):
    """
    this class defines the structure of the data that will be sent to the /auth/signup endpoint in the request body
    the data will be validated according to the rules defined in the methods of this class
    if the data is valid, a new user will be created and saved to the database
    """
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    username = serializers.CharField(max_length=150, required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "This email is already in use"})
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': "This username is already in use"})
        return username
    
    def validate_password1(self, password1):
        if len(password1) < 8:
            raise serializers.ValidationError({'error': "Password must be at least 8 characters long"})
        return password1
    
    def validate_password2(self, password2):
        password1 = self.initial_data.get('password1')
        if password1 != password2:
            raise serializers.ValidationError({'error': "The password don't match"})
        return password2


    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password1')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return user

