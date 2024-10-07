from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} token"


class Cat(models.Model):
    color = models.CharField(max_length=32, verbose_name="Цвет котенка")
    age = models.IntegerField(verbose_name="Возраст в месяцах котенка")
    description = models.TextField(verbose_name="Описание котенка")
    is_deleted = models.BooleanField(default=False)
    kind = models.ForeignKey(
        "Kind",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=False,
        verbose_name="Порода котенка",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=False,
        verbose_name="Владелец котенка",
    )

    class Meta:
        db_table = "cat"


class Kind(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название породы")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "kind"
