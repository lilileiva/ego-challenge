from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"])
        if user.exists():
            user = user.first()
            if not user.check_password(data["password"]):
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data

    def create(self, validated_data):
        login(self.context["request"], validated_data["user"])
        return validated_data["user"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"])
        if user.exists():
            raise serializers.ValidationError("Username already exists")
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["username"],
            username=validated_data["username"],
            password=validated_data["password"],
            is_staff=True,
            is_superuser=True,
        )
        user.save()
        return user
