# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser as MultipartParser

# Models
from ego.cars.models.features import Feature

# Serializer
from ego.cars.serializers.features import FeatureSerializer


class FeaturesViewSet(viewsets.ModelViewSet):

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultipartParser,)
