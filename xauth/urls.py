from xauth.views import UserViewSet
from rest_framework import routers, serializers, viewsets
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
