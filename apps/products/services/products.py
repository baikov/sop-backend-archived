# from django.db import transaction
from django.db.models.query import QuerySet

from apps.products.filters import ProductFilter
from apps.products.models import Product


def get_products_list(filters=None) -> QuerySet:
    """
    Возвращает список объектов. Реализована фильтрация.
    """
    filters = filters or {}
    qs = Product.objects.all()
    return ProductFilter(filters, qs).qs
