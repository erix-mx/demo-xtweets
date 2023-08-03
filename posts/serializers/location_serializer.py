
from rest_framework import serializers

from posts.models import Location


class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = ('latitude', 'longitude')