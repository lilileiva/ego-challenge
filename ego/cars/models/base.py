import uuid
from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date when object was created")
    udpated_at = models.DateTimeField(auto_now=True, help_text="Date when object was modified")

    class Meta:
        abstract = True
        ordering = ["-created_at"]
