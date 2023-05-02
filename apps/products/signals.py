import math

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from slugify import slugify

from apps.products.models import Product, ProductPropertyValue

# from apps.products.services.products import (
#     add_product_properties,
#     remove_redundant_product_properties,
# )


@receiver(pre_save, sender=Product)
def generate_slug_signal(sender, instance, **kwargs):
    if instance.slug == "":
        instance.slug = slugify(instance.name)


@receiver(post_save, sender=Product)
def manage_product_properties_signal(sender, instance, **kwargs):
    """
    Если указана главная категория - добавить нужные свойства к товару, удалить ненужные
    """
    # add_product_properties(instance)
    # remove_redundant_product_properties(instance)
    pass


@receiver(post_save, sender=ProductPropertyValue)
def calculate_prices_signal(sender, instance, **kwargs):
    """
    Если указана длина и вес тонны - рассчитываем вес штуки, цену метра и цену штуки
    """
    if instance.property.code == "ves-metra" and instance.product.ton_price:
        instance.product.meter_price = math.ceil(
            float(instance.product.ton_price)
            / 1_000
            * float(instance.value.replace(",", "."))
        )

        length = (
            ProductPropertyValue.objects.filter(
                product=instance.product,
                property__code="dlina",
            )
            .first()
            .value
        )
        if "-" in length:
            length = length.split("-")[0]

        if length:
            instance.product.unit_price = math.ceil(
                float(instance.product.meter_price) * float(length) / 1000
            )
        instance.product.save()

    if instance.property.code == "dlina" and instance.product.meter_price:
        length = instance.value
        if "-" in length:
            length = length.split("-")[0]

        if length:
            instance.product.unit_price = math.ceil(
                float(instance.product.meter_price) * float(length) / 1000
            )
            instance.product.save()
