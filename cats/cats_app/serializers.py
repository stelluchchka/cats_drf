from cats_app.models import Cat
from rest_framework import serializers


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["pk", "color", "age", "description"]
