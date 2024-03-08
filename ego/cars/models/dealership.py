import uuid
from django.db import models
from ego.utils.enums.provinces import Provinces


class Dealership(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    address = models.CharField(max_length=250, unique=True, help_text="Dealership address")
    province = models.CharField(
        choices=Provinces.choices, max_length=100, help_text="Dealership province"
    )
    phone = models.IntegerField(help_text="Dealership phone number")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date when dealership was created"
    )
    udpated_at = models.DateTimeField(
        auto_now=True, help_text="Date when dealership was modified"
    )

    def __str__(self):
        return self.address - self.province
