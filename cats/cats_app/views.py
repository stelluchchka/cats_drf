from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from cats_app.serializers import (
    CatSerializer,
    KindSerializer,
    CatDetailedSerializer,
    UserSerializer,
    LoginResponseSerializer,
)
from cats_app.models import Cat, Kind
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from cats_app.permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Никнейм"),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Электронная почта"
            ),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="Имя"),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Фамилия"
            ),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Пароль"),
        },
    ),
    operation_description="Регистрация нового пользователя",
    responses={
        201: openapi.Response("Успешная регистрация", UserSerializer),
        400: openapi.Response("Ошибка при регистрации"),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        user = serializer.save()
        user.set_password(request.data.get("password"))
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh.payload.update(
            {
                "user_id": user.id,
                "username": user.username,
                "is_superuser": user.is_superuser,
            }
        )

        return Response(
            {
                "user": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

    except ValidationError as ve:
        return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(
            {"error": "Пользователь с таким никнеймом уже существует"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Никнейм"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Пароль"),
        },
    ),
    operation_description="Авторизация пользователя",
    responses={
        200: openapi.Response("Успешная авторизация", LoginResponseSerializer),
        400: openapi.Response("Неверные учетные данные"),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        if not all([username, password]):
            raise PermissionDenied(detail="Необходимы оба поля: никнейм и пароль")

        user = authenticate(request, username=username, password=password)

        if not user:
            raise PermissionDenied(detail="Неверные учетные данные")

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({"user_id": user.id, "username": user.username})

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

    except PermissionDenied as e:
        return Response({"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING, description="Refresh token"
            ),
        },
    ),
    operation_description="Выход из системы",
    responses={
        200: openapi.Response("Успешный выход"),
        400: openapi.Response("Неверный refresh token или отсутствует refresh token"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Необходим Refresh token"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except Exception as e:
        return Response(
            {"error": "Неверный Refresh token"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"success": "Выход успешен"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    operation_description="Получение списка пород",
    responses={
        200: openapi.Response("Успех", KindSerializer),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_kinds(request, format=None):
    try:
        kinds = Kind.objects.all()
        serializer = KindSerializer(kinds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            name="kind",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Порода котенка для фильтрации",
            required=False,
        ),
    ],
    operation_description="Получение списка котят с возможностью фильтрации по породе",
    responses={
        200: openapi.Response("Успех", CatSerializer(many=True)),
        404: openapi.Response("Не найдено котят"),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_cats(request, format=None):
    try:
        filters = Q(is_deleted=False)
        target_kind_name = request.query_params.get("kind", None)
        if target_kind_name:
            target_kind = Kind.objects.get(name=target_kind_name)
            filters &= Q(kind=target_kind)
        cats = Cat.objects.filter(filters)
        serializer = CatSerializer(cats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "color": openapi.Schema(
                type=openapi.TYPE_STRING, description="Цвет котенка"
            ),
            "age": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Возраст котенка в месяцах"
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Описание котенка"
            ),
            "kind": openapi.Schema(
                type=openapi.TYPE_STRING, description="Порода котенка"
            ),
        },
    ),
    operation_description="Добавление нового котенка",
    responses={
        201: openapi.Response("Котенок успешно добавлен", CatDetailedSerializer),
        400: openapi.Response("Некорректные данные"),
        403: openapi.Response("Доступ запрещен"),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_cats(request):
    try:
        user = request.user
        serializer = CatDetailedSerializer(data=request.data)
        kind_name = request.data["kind"]
        kind, _ = Kind.objects.get_or_create(name=kind_name)
        if serializer.is_valid():
            serializer.save(kind=kind, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="get",
    operation_description="Получение подробной информации о котенке",
    responses={
        200: openapi.Response("Успех", CatDetailedSerializer),
        403: openapi.Response("Доступ запрещен"),
        404: openapi.Response("Не найдено котят"),
    },
)
@api_view(["GET"])
@permission_classes([IsOwnerOrReadOnly])
def get_cat(request, pk, format=None):
    try:
        cat = get_object_or_404(Cat.objects.filter(is_deleted=False), pk=pk)
        serializer = CatDetailedSerializer(cat)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="put",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "color": openapi.Schema(
                type=openapi.TYPE_STRING, description="Цвет котенка"
            ),
            "age": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Возраст котенка в месяцах"
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Описание котенка"
            ),
            "kind": openapi.Schema(
                type=openapi.TYPE_STRING, description="Порода котенка"
            ),
        },
    ),
    operation_description="Обновление информации о кошке",
    responses={
        200: openapi.Response("Успешное обновление", CatDetailedSerializer),
        400: openapi.Response("Некорректные данные"),
        403: openapi.Response("Доступ запрещен"),
        404: openapi.Response("Котенок не найден"),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["PUT"])
@permission_classes([IsOwnerOrReadOnly])
def put_cat(request, pk, format=None):
    try:
        cat = get_object_or_404(Cat, pk=pk)
        if cat.user != request.user:
            return Response(
                {"error": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN
            )
        cat_serializer = CatDetailedSerializer(cat, data=request.data, partial=True)
        kind_name = request.data.get("kind", None)
        if cat_serializer.is_valid():
            if kind_name:
                kind, _ = Kind.objects.get_or_create(name=kind_name)
                cat_serializer.save(kind=kind)
                return Response(cat_serializer.data)
            else:
                cat_serializer.save()
                return Response(cat_serializer.data)
        else:
            return Response(cat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="delete",
    operation_description="Удаление котенка",
    responses={
        200: openapi.Response("Успешное удаление"),
        403: openapi.Response("Доступ запрещен"),
        404: openapi.Response("Котенок не найден"),
        500: openapi.Response("Внутренняя ошибка сервера"),
    },
)
@api_view(["DELETE"])
@permission_classes([IsOwnerOrReadOnly])
def delete_cat(request, pk, format=None):
    try:
        cat = get_object_or_404(Cat, pk=pk)
        if cat.user != request.user:
            return Response(
                {"error": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN
            )
        cat.is_deleted = True
        cat.save()
        return Response(
            {"status": "success", "is_deleted": cat.is_deleted},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
