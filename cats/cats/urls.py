from django.contrib import admin
from cats_app import views
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('admin/', admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(r"kinds/", views.get_kinds, name="kinds-list"),
    path(r"cats/", views.Cats.as_view(), name="cats-list"),
    path(r"cats/<int:pk>/", views.CatDetail.as_view(), name="cat-detail"),
    path(r"filtered_cats/", views.get_filtered_cats, name="filtered_cats-list"),
]
