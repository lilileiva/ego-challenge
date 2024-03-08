# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

# Models
from ego.cars.models.reviews import Review

# Serializer
from ego.cars.serializers.reviews import ReviewSerializer


class ReviewViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.query_params.get("car") is not None:
            return self.queryset.filter(car__pk=self.request.query_params.get("car"))
        return self.queryset
