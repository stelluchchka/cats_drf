from django.db import models

class Cat(models.Model):
    color = models.CharField(max_length=32, verbose_name="Цвет котенка")
    age = models.IntegerField(verbose_name="Возраст в месяцах")
    description = models.TextField(verbose_name="Описание")

class Kind(models.Model):
    name = models.CharField(max_length=32, verbose_name="Название породы")