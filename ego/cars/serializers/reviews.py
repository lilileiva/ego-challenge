# Django REST Framework
from rest_framework import serializers

# Models
from ego.cars.models.reviews import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
