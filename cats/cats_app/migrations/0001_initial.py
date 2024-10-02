# Generated by Django 5.1.1 on 2024-10-02 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=32, verbose_name="Цвет котенка")),
                ("age", models.IntegerField(verbose_name="Возраст в месяцах")),
                ("description", models.TextField(verbose_name="Описание")),
            ],
        ),
    ]
