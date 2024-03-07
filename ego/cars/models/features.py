import uuid
from django.db import models


class Feature(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(help_text="Feature image", upload_to="features")
    title = models.CharField(max_length=100, help_text="Feature title")
    description = models.TextField(max_length=500, help_text="Feature description")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date when feature was created"
    )
    udpated_at = models.DateTimeField(
        auto_now=True, help_text="Date when feature was modified"
    )

    class Meta:
        unique_together = ("title", "description")
