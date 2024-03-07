# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# Models
from ego.cars.models.features import Feature

# Serializer
from ego.cars.serializers.features import FeatureSerializer


class FeaturesViewSet(viewsets.ModelViewSet):

    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
