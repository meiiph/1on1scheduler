from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

class UserSerializer(serializers.ModelSerializer):
    """
    serializer for the user model. validates the post request sent to the endpoint
    accounts/signup.
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def validate_password(self, value):
        """
        validates password by ensuring it has at least 8 characters and at most 100.
        """
        validate_password(value)
        if len(value) < 8:
            raise serializers.ValidationError("password must be at least 8 characters.")
        elif len(value) > 100:
            raise serializers.ValidationError("password must be less than 100 characters.")
        return value
    
    def validate_email(self, value):
        """
        validates email using django's built in email validator. also checks to see
        if the email is already in use. 
        """
        validate_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("this email address is already in use.")
        return value
    
    def validate_username(self, value):
        """
        validates the username by checking if its already in use. the username must also
        be greater than 4 charcters and less than 50. 
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("this username is already in use.")
        elif len(value) < 4:
            raise serializers.ValidationError("username must be greater than 4 characters.")
        elif len(value) > 50:
            raise serializers.ValidationError("username must be less than 50 characters.")
        return value
    
    def validate_first_name(self, value):
        """
        validates the first name by checking that the field only contains letters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("first name must contain only letters.")
        return value[0].upper() + value[1:].lower()
    
    def validate_last_name(self, value):
        """
        validates the last name by checking that the field only contains letters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("last name must contain only letters.")
        return value[0].upper() + value[1:].lower()
    
    def create(self, validated_data):
        """
        creates and activates a user.
        """
        validated_data['is_active'] = True
        validated_data['is_staff'] = False
        user = User.objects.create_user(**validated_data)
        return user
    
    def to_representation(self, instance):
        """
        returns a json representation of a user with the following fields:
        username, first_name, last_name.
        """
        return {'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name} 