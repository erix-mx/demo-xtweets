from django.db import models
import uuid

# Create your models here.
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
        