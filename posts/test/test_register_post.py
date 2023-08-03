from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class TestPostCase(TestCase):
  
  def setUp(self):
    self.client = APIClient()
    User = get_user_model()
    self.user = User.objects.create(email='demo@user.com', password='demopassword123', username='demo')
    refresh = RefreshToken.for_user(self.user)
    self.token = str(refresh.access_token)
    self.token_refresh = str(refresh)
    
    self.client_auth = APIClient(HTTP_AUTHORIZATION='Bearer ' + self.token)
      
  def test_success_post(self):    
    data = {
      "content": "Test content for a post",
      "imageUrl": "",
      "videoUrl": "",
      "location": {
        "latitude": "99.00",
        "longitude": "88.0"
      }
    }
    response = self.client_auth.post('/v1/post/', data, format='json')     
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
  def test_unauthorized_post(self):
    data = {
        "content": "Test content for a post",
        "imageUrl": "",
        "videoUrl": "",
        "location": {
            "latitude": "99.00",
            "longitude": "88.00"
        }
    }
    response = self.client.post('/v1/post/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
  def test_missing_fields(self):
    data = {
        "imageUrl": "",  # 'content' field is missing
        "videoUrl": "",
        "location": {
            "latitude": "99.00",
            "longitude": "88.0"
        }
    }
    response = self.client_auth.post('/v1/post/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('content', response.data['error'])

    data = {
        "content": "Test content for a post",
        "imageUrl": "",
        "videoUrl": "",
        # 'location' field is missing
    }
    response = self.client_auth.post('/v1/post/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)    
    
  def test_invalid_location_data(self):
    data = {
        "content": "Test content for a post",
        "imageUrl": "",
        "videoUrl": "",
        "location": {
            "latitude": "invalid_latitude",
            "longitude": "88.0"
        }
    }
    response = self.client_auth.post('/v1/post/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    

    data = {
        "content": "Test content for a post",
        "imageUrl": "",
        "videoUrl": "",
        "location": {
            "latitude": "99.00",
            "longitude": "invalid_longitude"
        }
    }
    response = self.client_auth.post('/v1/post/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    
    
  def test_create_post_with_required_fields(self):
    data = {
        "content": "Test content for a post",        
    }
    response = self.client_auth.post('/v1/post/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
  
    
    
    
    
    