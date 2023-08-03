import uuid

from django.contrib.auth import get_user_model
from django.db import models


class UUIDModel(models.Model):
    """
    Minimal models attrs
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Location(UUIDModel):
  latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
  longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

class Post(UUIDModel):
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  imageUri = models.URLField(blank=True, null=True)
  videoUri = models.URLField(blank=True, null=True)
  content = models.TextField(blank=False)
  location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
  