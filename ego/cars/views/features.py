# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser as MultipartParser
from rest_framework.parsers import JSONParser as JSONParser

# Models
from ego.cars.models.features import Feature

# Serializer
from ego.cars.serializers.features import FeatureSerializer


class FeaturesViewSet(viewsets.ModelViewSet):

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultipartParser, JSONParser)

    def get_permissions(self):
        if self.request.method != "GET":
            return [IsAuthenticated(), IsAdminUser()]
        else:
            return [AllowAny()]
