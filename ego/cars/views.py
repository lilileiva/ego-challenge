# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class CarsViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=["get"])
    def test(self, request):
        return Response(data="test", status=status.HTTP_200_OK)