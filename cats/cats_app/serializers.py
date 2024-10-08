from cats_app.models import Cat, Kind, User
from rest_framework import serializers


class CatSerializer(serializers.ModelSerializer):
    kind = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cat
        fields = ["pk", "kind"]


class CatDetailedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    kind = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cat
        fields = ["pk", "color", "age", "description", "user", "kind"]


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = ["pk", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, allow_blank=False)
    access = serializers.CharField(required=True, allow_blank=False)
