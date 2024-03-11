# Django REST Framework
from rest_framework import serializers

# Models
from ego.cars.models.cars import Car
from ego.cars.models.features import Feature
from ego.cars.serializers.reviews import ReviewSerializer


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class AddFeatureSerializer(serializers.Serializer):
    feature_id = serializers.UUIDField()

    def validate(self, data):
        feature = Feature.objects.filter(uuid=data["feature_id"])
        car = Car.objects.filter(uuid=self.context["car_id"])
        if not feature.exists():
            raise serializers.ValidationError("Feature does not exists")
        if not car.exists():
            raise serializers.ValidationError("Car does not exists")
        data["car_id"] = self.context["car_id"]
        return data

    def create(self, validated_data):
        car = Car.objects.get(uuid=validated_data["car_id"])
        feature = Feature.objects.get(uuid=validated_data["feature_id"])
        car.add_feature(feature)
        car.save()
        return car


class GetCarReviewsSerializer(serializers.Serializer):
    car_id = serializers.UUIDField()

    def validate(self, data):
        car = Car.objects.filter(uuid=data["car_id"])
        if not car.exists():
            raise serializers.ValidationError("Car does not exists")
        return data

    def create(self, validated_data):
        car = Car.objects.get(uuid=validated_data["car_id"])
        avg_rating = car.get_average_rating()
        reviews = [
            {
                "comment": review.comment,
                "stars": review.stars,
                "created_at": review.created_at,
            }
            for review in car.get_reviews()
        ]
        return avg_rating, reviews
