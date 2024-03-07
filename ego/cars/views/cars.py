# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter

# Models
from ego.cars.models.cars import Car

# Serializer
from ego.cars.serializers.cars import CarSerializer


class CarsViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all().order_by("-created_at")
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "year"]
