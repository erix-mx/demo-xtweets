from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
# Create your tests here.
class TestRegisterCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    User = get_user_model()
    self.user = User.objects.create_user(
        email='demo@user.com', username='demo', first_name="Pepito")
    self.user.set_password('pepito123')
    self.user.save()
  
  def test_success_register(self):    
    data = {
        'email': 'demo2@user.com',
        'password': 'pepito123',
        'username': 'demo2',
    }
    response = self.client.post('/v1/register/', data, format='json')     
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_user_was_registered_by_email(self):    
    data = {
        'email': 'demo@user.com',
        'password': 'pepito123',
        'username': 'demo3',
    }
    response = self.client.post('/v1/register/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
  
  def test_user_was_registered_by_user(self):    
    data = {
        'email': 'demo3@user.com',
        'password': 'pepito123',
        'username': 'demo',
    }
    response = self.client.post('/v1/register/', data, format='json')    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  
  def test_when_email_is_invalid(self):
    data = {
        'email': 'no_email',
        'password': 'no_email123',
        'username': 'no_email',
    }
    response = self.client.post('/v1/register/', data, format='json')      
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  
  