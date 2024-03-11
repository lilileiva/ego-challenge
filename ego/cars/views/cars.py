# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser as MultipartParser
from rest_framework.parsers import JSONParser as JSONParser
from rest_framework.parsers import FileUploadParser as FileUploadParser

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
    parser_classes = (MultipartParser, JSONParser, FileUploadParser)
    lookup_field = "pk"

    def get_permissions(self):
        if self.action == "add_feature":
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method != "GET":
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]

    @swagger_auto_schema(
        methods=["post"],
        request_body=AddFeatureSerializer,
        responses=add_feature_responses,
        operation_description="Add a feature to specific car",
    )
    @action(detail=True, methods=["post"])
    def add_feature(self, request, pk):
        serializer = AddFeatureSerializer(data=request.data, context={"car_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["get"],
        responses=reviews_responses,
        operation_description="Get all reviews of specific car",
    )
    @action(detail=True, methods=["get"])
    def reviews(self, request, pk):
        serializer = GetCarReviewsSerializer(data={"car_id": pk})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response = {"avg_rating": data[0], "reviews": data[1]}
        return Response(response, status.HTTP_200_OK)
