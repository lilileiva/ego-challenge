# Django REST Framework
from rest_framework import serializers

# Models
from ego.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
