from django.db import models

class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'user'


class Cat(models.Model):
    color = models.CharField(max_length=32, verbose_name="Цвет котенка")
    age = models.IntegerField(verbose_name="Возраст в месяцах котенка")
    description = models.TextField(verbose_name="Описание котенка")
    is_deleted = models.BooleanField(default=False)
    kind = models.ForeignKey('Kind', on_delete=models.DO_NOTHING, null=True, blank=False, verbose_name="Порода котенка")
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=False, verbose_name="Владелец котенка")

    class Meta:
        db_table = 'cat'

class Kind(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название породы")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'kind'