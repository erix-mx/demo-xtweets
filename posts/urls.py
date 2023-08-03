
from django.urls import include, path
from rest_framework import routers

from posts.views.view_post import PostViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')


urlpatterns = [
    path('', include(router.urls))
]
