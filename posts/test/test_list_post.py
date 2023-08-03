from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Post


# Create your tests here.
class TestPostListCase(TestCase):
  
  def setUp(self):
    self.client = APIClient()
    
    User = get_user_model()
    self.user = User.objects.create(email='demo@user.com', password='demopassword123', username='demo')
    self.user_2 = User.objects.create(email='user2@user.com', password='demopassword123', username='user2')
    
    refresh = RefreshToken.for_user(self.user)
    self.token = str(refresh.access_token)
    self.token_refresh = str(refresh)
    
    self.client_auth = APIClient(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    posts = [
      Post(
          author=self.user,
          content=f"Test content for post {i}",
          imageUri=f"image_url_{i}.jpg",
          videoUri=f"video_url_{i}.mp4",
      )
      for i in range(1, 101)
    ]
    Post.objects.bulk_create(posts)
    
    self.first_post = Post.objects.all().first()
  
  def test_success_list_posts(self):
    response = self.client_auth.get('/v1/post/', format='json')    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 20)
  
  def test_success_list_posts_page_2(self):
    response = self.client_auth.get('/v1/post/?page=2', format='json')    
    self.assertEqual(response.status_code, status.HTTP_200_OK) 
    self.assertEqual(len(response.data['results']), 20)
  
  def test_success_delete_post_by_owner(self):
    new_post = Post.objects.create(
        author=self.user,
        content=f"Test content for post",
        imageUri=f"image_url.jpg",
        videoUri=f"video_url.mp4",
    )    
    response = self.client_auth.delete(f'/v1/post/{new_post.uuid}/')        
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)    
    self.assertEqual(Post.objects.count(), 100)
    
  def test_delete_post_by_reader(self):
    new_post = Post.objects.create(
        author=self.user_2,
        content=f"Test content for post",
        imageUri=f"image_url.jpg",
        videoUri=f"video_url.mp4",
    ) 
    response = self.client_auth.delete(f'/v1/post/{new_post.uuid}/')        
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
    self.assertEqual(Post.objects.count(), 101)