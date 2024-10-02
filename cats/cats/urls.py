from django.contrib import admin
from cats_app import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'cats/', views.Cats.as_view(), name='cats-list'),
    path(r'cats/<int:pk>/', views.CatDetail.as_view(), name='cat-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]