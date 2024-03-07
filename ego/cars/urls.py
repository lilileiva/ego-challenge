from django.urls import include, path
from . import views as cars_views

# Django REST Framework
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register(r"cars", cars_views.CarsViewSet, basename="cars")
router.register(r"features", cars_views.FeaturesViewSet, basename="features")

urlpatterns = [path("", include(router.urls))]
