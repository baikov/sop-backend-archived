from django.db.models.query import QuerySet
from rest_framework.exceptions import NotFound

from apps.products.filters import ProductFilter
from apps.products.models import Category
from apps.utils.custom import get_object_or_None


def get_category_list() -> QuerySet:
    """
    Возвращает список объектов. Реализована фильтрация.
    """
    qs = Category.objects.filter(is_published=True)
    return qs


def get_root_categories() -> QuerySet:
    """
    Возвращает список объектов. Реализована фильтрация.
    """
    qs = Category.get_root_nodes()
    return qs


def get_children_categories(slug: str):
    category = get_object_or_None(Category, slug=slug)
    if category is None:
        raise NotFound(f"Категория slug={slug} не существует")

    return category.get_descendants().filter(is_published=True)


def get_category_product_list(slug: str, filters: dict = None):
    filters = filters or {}

    category = get_object_or_None(Category, slug=slug)
    if category is None:
        raise NotFound(f"Категория slug={slug} не существует")
    qs = category.products.filter(is_published=True)
    return ProductFilter(filters, qs).qs
