from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
# Create your tests here.
class TestAuthCase(TestCase):
  
  def setUp(self):
    self.client = APIClient()
    User = get_user_model()
    self.user = User.objects.create_user(
        email='demo@user.com', username='demo', first_name="Pepito")
    self.user.set_password('pepito123')
    self.user.save()
  
  def test_success_auth(self):    
    data = {
        'email': 'demo@user.com',
        'password': 'pepito123',
    }
    response = self.client.post('/v1/auth/', data, format='json')        
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_fail_auth(self):    
    data = {
        'email': '',
        'password': '', 
    }
    response = self.client.post('/v1/auth/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  
  def test_password_was_wrong(self):
    data = {
        'email': 'demo@user.com',
        'password': 'pepito123z',
    }
    response = self.client.post('/v1/auth/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  
  def test_email_was_wrong(self):
    data = {
        'email': 'demo@userr.com',
        'password': 'pepito123',
    }
    response = self.client.post('/v1/auth/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  
  def test_method_not_allowed(self):
    response = self.client.get('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'GET')
    
    response = self.client.put('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'PUT')
    
    response = self.client.delete('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'DELETE')
    
    response = self.client.patch('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'PATCH')
    
    response = self.client.head('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'HEAD')
    
    response = self.client.options('/v1/auth/')    
    self.assertEqual(response.status_code, status.HTTP_200_OK, 'OPTIONS')
    
    response = self.client.trace('/v1/auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, 'TRACE')
    
    
    