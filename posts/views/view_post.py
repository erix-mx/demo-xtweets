from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.viewsets import GenericViewSet
from posts.models import Post

from posts.serializers.post_serializer import PostSerializer
from posts.utils.base_permission import IsAuthorOrReadOnly
from posts.utils.custom_pagination import CustomPagination


class PostViewSet(GenericViewSet):
  """
  A ViewSet to handle registration of new posts.

  The `post` method in this ViewSet allows authenticated users to create new posts.
  """
  serializer_class = PostSerializer
  lookup_field = 'uuid'
  queryset = Post.objects.all()
  permission_classes = [IsAuthenticated]
  
  def get_permissions(self):
    if self.action == 'destroy':
      self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    else:
      self.permission_classes = [IsAuthenticated]
    return super().get_permissions()
  
  @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
  def post(self, request):
    """
    Create a new post.

    This method allows authenticated users to create new posts. The request data should
    include the necessary fields to create a new post. If the data is valid, the new post
    will be saved to the database and a response with the created post's data will be returned.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A response object containing the created post's data and a status code.
                  If there are validation errors, a response with the error details and
                  a 400 status code will be returned.
    """
    data = request.data    
    serializer = PostSerializer(data=data, context={'request': request})
    is_valid = serializer.is_valid()
    if is_valid:
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def list(self, request):
    """   
    """
    queryset = Post.objects.all().order_by('-created')  # Retrieve all posts from the database
    paginator = CustomPagination()  # Instantiate the pagination class
    paginated_queryset = paginator.paginate_queryset(queryset, request)  # Paginate the queryset
    serializer = PostSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)
        
  def destroy(self, request, uuid=None):
    """
    Delete a post.

    This method allows authenticated users to delete a post. The request data should
    include the necessary fields to delete a post. If the data is valid, the post
    will be deleted from the database and a response with the deleted post's data will be returned.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A response object containing the deleted post's data and a status code.
                  If there are validation errors, a response with the error details and
                  a 400 status code will be returned.
    """    
    post = self.get_object()
    post.delete()
    return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)