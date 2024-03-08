# Django REST Framework
from rest_framework import serializers

# Models
from ego.cars.models.dealership import Dealership


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
