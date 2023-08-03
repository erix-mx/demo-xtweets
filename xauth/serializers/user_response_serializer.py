from django.db import models
from rest_framework import serializers

from xauth.serializers.user_serializer import UserSerializer

class UserResponseSerializer(serializers.Serializer):
  user = UserSerializer()
  token = serializers.CharField(max_length=255)