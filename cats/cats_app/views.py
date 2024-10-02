from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from cats_app.serializers import CatSerializer
from cats_app.models import Cat
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class Cats(APIView):
    model_class = Cat
    serializer_class = CatSerializer

    def get(self, request, format=None):
        cats = self.model_class.objects.all()
        serializer = self.serializer_class(cats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CatDetail(APIView):
    model_class = Cat
    serializer_class = CatSerializer

    def get(self, request, pk, format=None):
        cat = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(cat)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cat = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cat = get_object_or_404(self.model_class, pk=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

