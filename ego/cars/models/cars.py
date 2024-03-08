import uuid
from django.db import models
from ego.utils.enums.cars_types import CarsTypes
from ego.cars.models.reviews import Review


class Car(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    car_type = models.CharField(
        max_length=50, choices=CarsTypes.choices, help_text="Car type"
    )
    model = models.CharField(max_length=100, help_text="Car model name")
    year = models.IntegerField(help_text="Car year of production")
    price = models.IntegerField(help_text="Car price in ARS")
    image = models.ImageField(help_text="Car image", upload_to="cars")
    title = models.CharField(max_length=100, help_text="Car brief description")
    description = models.TextField(max_length=500, help_text="Car extended description")
    features = models.ManyToManyField(
        "cars.Feature", null=True, blank=True, help_text="Car features"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date when car was created"
    )
    udpated_at = models.DateTimeField(
        auto_now=True, help_text="Date when car was modified"
    )

    class Meta:
        unique_together = ("car_type", "model", "year")

    def __str__(self):
        return self.model

    def get_reviews(self):
        reviews = Review.objects.filter(car=self.uuid).order_by("-created_at")
        return list(reviews)

    def get_average_rating(self):
        reviews = self.get_reviews()
        if reviews:
            return sum([review.stars for review in reviews]) / len(reviews)
        return 0

    def add_feature(self, feature):
        self.features.add(feature)
        self.save()
        return self