from enum import Enum
from django.db import models


class CarsTypes(models.TextChoices):
    AUTOS = "Autos"
    PICKAUPS_Y_COMERCIALES = "Pickups y Comerciales"
    SUVS_Y_CROSSOVERS = "SUVs y Crossovers"
