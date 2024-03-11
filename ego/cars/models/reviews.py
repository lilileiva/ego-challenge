from django.db import models
from ego.cars.models.base import BaseModel


class Review(BaseModel):
    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE)
    stars = models.IntegerField(choices=((i, i) for i in range(1, 6)), help_text="Qualification of the car")
    comment = models.CharField(max_length=250, help_text="Review comment")

    def __str__(self):
        return f"{self.comment} ({self.stars})"
