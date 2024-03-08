# Django
from django.contrib import admin

# Models
from ego.cars.models import Car
from ego.cars.models.dealership import Dealership
from ego.cars.models.features import Feature
from ego.cars.models.reviews import Review


class CarsAdmin(admin.ModelAdmin):
    list_display = ["uuid", "model", "price", "year", "car_type"]
    ordering = ["uuid"]
    list_filter = ["car_type"]


admin.site.register(Car, CarsAdmin)


class FeaturesAdmin(admin.ModelAdmin):
    list_display = ["uuid", "title", "description", "car"]
    ordering = ["uuid"]


admin.site.register(Feature, FeaturesAdmin)


class DealershipsAdmin(admin.ModelAdmin):
    list_display = ["uuid", "province", "address", "phone"]
    ordering = ["uuid"]
    list_filter = ["province"]


admin.site.register(Dealership, DealershipsAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ["uuid", "stars", "comment", "car"]
    ordering = ["uuid"]
    list_filter = ["car", "stars"]


admin.site.register(Review, ReviewsAdmin)
