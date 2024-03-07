from django.urls import include, path
from . import views as cars_views

# Django REST Framework
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register(r'cars', cars_views.CarsViewSet, basename='cars')

urlpatterns = [
    path('', include(router.urls))
]
