from django.db import models
from ego.cars.models.base import BaseModel
from ego.utils.enums.provinces import Provinces


class Dealership(BaseModel):
    address = models.CharField(max_length=250, unique=True, help_text="Dealership address")
    province = models.CharField(choices=Provinces.choices, max_length=100, help_text="Dealership province")
    phone = models.IntegerField(help_text="Dealership phone number")

    def __str__(self):
        return f"{self.address} - {self.province}"
