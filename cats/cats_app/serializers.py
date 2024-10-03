from cats_app.models import Cat, Kind
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
