from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from loguru import logger  # noqa F401
from slugify import slugify

from apps.products.models import Product, ProductPropertyValue
from apps.products.services.products import (
    add_product_properties,
    remove_redundant_product_properties,
)


@receiver(pre_save, sender=Product)
def calculate_prices_signal(sender, instance, **kwargs):
    # 3. Калькуляция цен
    # 4. Заполнение slug + уникализация

    if instance.slug == "":
        instance.slug = slugify(instance.name)
    # replacements=[['|', 'or'], ['%', 'percent']]
    # if instance.pk:
    #     try:
    #         orig = sender.objects.get(id=instance.id)
    #         if orig:
    #             changes = 0
    #             for field in input_fields:
    #                 if not (getattr(instance, field)) == (getattr(orig, field)):
    #                     changes += 1
    #             if changes > 0:
    #                 # do something here because at least one field changed...
    #                 my_geocoder_function(instance)
    #     except:
    #         # do something here because there is no original, or pass.
    #         my_geocoder_function(instance)

    # else:
    if instance.ton_price:
        try:
            meter_weight = instance.properties_through.get(
                property__code="ves-metra"
            ).value
            instance.meter_price = (
                instance.ton_price
                / 1_000_000
                * int(float(meter_weight.replace(",", ".")) * 1000)
            )
        except ProductPropertyValue.DoesNotExist:
            pass
        try:
            unit_weight = instance.properties_through.get(
                property__code="ves-shtuki"
            ).value
            instance.unit_price = (
                instance.ton_price
                / 1_000_000
                * int(float(unit_weight.replace(",", ".")) * 1000)
            )
        except ProductPropertyValue.DoesNotExist:
            pass
        # instance.meter_price = instance.ton_price / 1_000_000 * int(meter_weight)
        # instance.unit_price = instance.ton_price / 1_000_000 * int(unit_weight)


@receiver(post_save, sender=Product)
def manage_product_properties_signal(sender, instance, **kwargs):
    # 1. Если выбрана категория - добавить нужные свойства к товару
    add_product_properties(instance)
    remove_redundant_product_properties(instance)
    # 2. Если указана длина и вес метра - рассчитать вес штуки
