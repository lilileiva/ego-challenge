from django.urls import include, path
from . import views as cars_views

# Django REST Framework
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register(r"cars", cars_views.CarsViewSet, basename="cars")
router.register(r"features", cars_views.FeaturesViewSet, basename="features")
router.register(r"dealership", cars_views.DealershipViewSet, basename="dealership")
router.register(r"reviews", cars_views.ReviewViewSet, basename="reviews")

urlpatterns = [path("", include(router.urls))]
