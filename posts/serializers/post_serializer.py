from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Location, Post
from posts.serializers.location_serializer import LocationSerializer
from xauth.serializers.user_serializer import UserSerializer

class PostSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True) 
  location = LocationSerializer(allow_null=True, required=False)  
  
  class Meta:
    model = Post
    fields = ('content', 'location', 'imageUri', 'videoUri', 'author', 'uuid', 'created', 'updated')    
    depth = 1
  
  def create(self, validated_data):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      author = request.user  
      location_data = validated_data.pop('location', None)
          
      post = Post.objects.create(author=author, **validated_data)
      if location_data is not None:
        location = Location.objects.create(**location_data)
        post.location = location
        post.save()
      
      return post
    else:
      raise serializers.ValidationError("User must be authenticated")