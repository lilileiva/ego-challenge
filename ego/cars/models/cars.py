from django.db import models
from ego.utils.enums.cars_types import CarsTypes


class Car(models.Model):
    car_type = models.CharField(max_length=50, choices=CarsTypes.choices)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        unique_together = ('car_type', 'model', 'year')

    def __str__(self):
        return self.model