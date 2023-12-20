from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequests

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class FriendRequestsSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = '__all__'