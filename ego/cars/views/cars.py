# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# Models
from ego.cars.models import Car

# Serializer
from ego.cars.serializers import CarSerializer



class CarsViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"])
    def test(self, request):
        return Response(data="test", status=status.HTTP_200_OK)