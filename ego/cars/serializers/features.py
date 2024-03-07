# Django REST Framework
from rest_framework import serializers

# Models
from ego.cars.models.features import Feature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
