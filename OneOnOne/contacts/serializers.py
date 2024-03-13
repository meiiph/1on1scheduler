from rest_framework import serializers
from .models import Contact
from django.contrib.auth.models import User

class ContactSerializer(serializers.ModelSerializer):
    # curr_user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only = True,
    # )
    contact_user = serializers.SlugRelatedField(
        slug_field='username',
        read_only = True,
        # queryset=User.objects.all(),
    )

    class Meta:
        model = Contact
        fields = ['id', 'contact_user', 'name', 'email']  
