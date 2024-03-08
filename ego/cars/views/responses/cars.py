"""Cars View responses"""

# Django REST Framework
from rest_framework import serializers
from rest_framework import status

# Swagger
from drf_yasg import openapi


class GetCarReviewsResponseSerializer(serializers.Serializer):
    """Api status response serializer.

    Will be used only for swagger reasons
    """

    avg_rating = serializers.FloatField()
    reviews = serializers.ListField()


reviews_response = openapi.Response(
    "Status of each api", GetCarReviewsResponseSerializer
)
reviews_responses = {
    status.HTTP_200_OK: reviews_response,
}
add_feature_response = openapi.Response("Status of each api", None)
add_feature_responses = {
    status.HTTP_200_OK: add_feature_response,
}
