# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser as MultipartParser
from rest_framework.parsers import JSONParser as JSONParser
from rest_framework.parsers import FileUploadParser as FileUploadParser
from rest_framework.response import Response

# Models
from ego.cars.models.cars import Car

# Serializer
from ego.cars.serializers.cars import (
    CarSerializer,
    GetCarReviewsSerializer,
    AddFeatureSerializer,
)

# Swagger
from drf_yasg.utils import swagger_auto_schema
from ego.cars.views.responses.cars import reviews_responses, add_feature_responses


class CarsViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all().order_by("-created_at")
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "year"]
    parser_classes = (
        MultipartParser,
        JSONParser,
    )

    @swagger_auto_schema(
        methods=["post"],
        request_body=AddFeatureSerializer,
        responses=add_feature_responses,
    )
    @action(detail=False, methods=["post"])
    def add_feature(self, request):
        serializer = AddFeatureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["post"],
        request_body=GetCarReviewsSerializer,
        responses=reviews_responses,
    )
    @action(detail=False, methods=["post"])
    def reviews(self, request):
        serializer = GetCarReviewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response = {"avg_rating": data[0], "reviews": data[1]}
        return Response(response, status.HTTP_200_OK)
