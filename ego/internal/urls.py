from django.urls import include, path
from . import views as internal_views

# Django REST Framework
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register(r"internal", internal_views.AccountsViewSet, basename="internal")

urlpatterns = [path("", include(router.urls))]
