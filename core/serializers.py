from abc import ABC

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        password_repeat = data.pop("password_repeat", None)
        if password != password_repeat:
            raise ValidationError("Password and password_repeat don't match")
        if not User.objects.filter(username=username).exists():
            raise ValidationError("Username is already in use")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.user = user
        return user


class LoginSerializer(serializers.Serializer, ABC):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Username or password not correct")
        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = ("old_password", "new_password")

    def validate(self, data):
        old_password = data.get("old_password")
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError({"old_password": "field not correct"})
        return data

    def update(self, example, validated_data):
        example.set_password(validated_data["new_password"])
        example.save(update_fields=["password"])
        return example
