import uuid
from django.db import models


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE)
    stars = models.IntegerField(
        choices=((i, i) for i in range(1, 6)), help_text="Qualification of the car"
    )
    comment = models.CharField(max_length=250, help_text="Review comment")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date when dealership was created"
    )
    udpated_at = models.DateTimeField(
        auto_now=True, help_text="Date when dealership was modified"
    )

    def __str__(self):
        return f"{self.comment} ({self.stars})"
