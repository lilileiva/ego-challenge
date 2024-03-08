# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser as MultipartParser
from rest_framework.parsers import JSONParser as JSONParser

# Models
from ego.cars.models.cars import Car

# Serializer
from ego.cars.serializers.cars import (
    CarSerializer,
    GetCarReviewsSerializer,
    AddFeatureSerializer,
)
from rest_framework.response import Response


class CarsViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all().order_by("-created_at")
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "year"]
    parser_classes = (MultipartParser, JSONParser)

    @action(detail=False, methods=["post"])
    def add_feature(self, request):
        serializer = AddFeatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def reviews(self, request):
        serializer = GetCarReviewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response = {"avg_rating": data[0], "reviews": data[1]}
        return Response(response, status.HTTP_200_OK)
