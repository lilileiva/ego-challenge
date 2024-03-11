from django.db import models
from ego.cars.models.base import BaseModel


class Feature(BaseModel):
    image = models.ImageField(help_text="Feature image", upload_to="features")
    title = models.CharField(max_length=100, help_text="Feature title")
    description = models.TextField(max_length=500, help_text="Feature description")

    class Meta:
        unique_together = ("title", "description")
