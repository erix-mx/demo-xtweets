
from django.urls import include, path
from rest_framework import routers

from xauth.views.view_auth import UserAuthViewSet
from xauth.views.view_register import UserRegisterViewSet

router = routers.DefaultRouter()
router.register(r'', UserAuthViewSet, basename='user_auth')
router.register(r'', UserRegisterViewSet, basename='user_register')

urlpatterns = [
    path('', include(router.urls))
]
