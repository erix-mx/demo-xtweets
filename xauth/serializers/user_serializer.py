
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):  
  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', )
    extra_kwargs = {
      'password': {'write_only': True},
      'email': {'required': True},
    }
    
  def validate_email(self, value):
      try:
          validate_email(value)
      except ValidationError:
          raise serializers.ValidationError('Invalid email format.')
      return value


