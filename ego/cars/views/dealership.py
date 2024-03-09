# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# Models
from ego.cars.models.dealership import Dealership

# Serializer
from ego.cars.serializers.dealership import DealershipSerializer


class DealershipViewSet(viewsets.ModelViewSet):

    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method != "GET":
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]
