from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="Название продукта", max_length=500)
    description = models.TextField(verbose_name="Описание", max_length=1500, blank=True)
    price = models.DecimalField(
        verbose_name="Цена", max_digits=20, decimal_places=2, default=0.00
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
