
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from xauth.serializers.user_response_serializer import UserResponseSerializer
from xauth.serializers.user_serializer import UserSerializer


class UserAuthViewSet(GenericViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  
  @action(detail=False, methods=['post'], permission_classes=[AllowAny])
  def auth(self, request):
    """
    Custom Authentication API Endpoint
    
    This method defines a custom authentication API endpoint for user login. It allows users to log in using their email and password and returns the user data along with a valid access token.

    :param request: The HTTP request object with the user credentials in the JSON body.
    :return: A JSON response containing the user data and the access token upon successful authentication, or an error response if the credentials are invalid or missing.
    """
    data = request.data
    
    # Ensure email and password are present in the JSON data
    if 'email' not in data or 'password' not in data:
      return Response({'error': 'Missing credentials in JSON data'}, status=status.HTTP_400_BAD_REQUEST)
    
    email = data['email']
    password = data['password']
    
    try:
      # Attempt to find the user by email
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
    
     # Authenticate the user with provided email and password
    user = authenticate(username=user.username, password=password)
    
    if user is not None:
       # Generate a JWT access token using SimpleJWT
      refresh = RefreshToken.for_user(user)
      access_token = str(refresh.access_token)
      
      # Serialize the user data to be returned in the response
      serializerResponse = UserResponseSerializer({
        'user': user,
        'token': access_token
      })      
      return Response(serializerResponse.data)
    else:
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
  