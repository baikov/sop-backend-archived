# Generated by Django 4.1.7 on 2023-03-08 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attribute",
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
                (
                    "name",
                    models.CharField(max_length=250, verbose_name="Название атрибута"),
                ),
                (
                    "description",
                    models.CharField(max_length=2500, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Свойство товара",
                "verbose_name_plural": "Свойства товаров",
            },
        ),
        migrations.CreateModel(
            name="AttributeValue",
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
                (
                    "value",
                    models.CharField(max_length=250, verbose_name="Название атрибута"),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="products.attribute",
                    ),
                ),
            ],
            options={
                "verbose_name": "Значение свойства",
                "verbose_name_plural": "Значения свойств",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="properties",
            field=models.ManyToManyField(
                related_name="products",
                to="products.attributevalue",
                verbose_name="Свойства",
            ),
        ),
    ]