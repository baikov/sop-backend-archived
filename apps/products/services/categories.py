from django.db.models import CharField, F, FloatField, Func, OuterRef, Subquery, Value
from django.db.models.functions import Cast
from django.db.models.query import QuerySet
from rest_framework.exceptions import NotFound

from apps.products.filters import ProductFilter
from apps.products.models import Category, ProductPropertyValue
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


def get_children_categories(slug: str) -> QuerySet:
    category = get_object_or_None(Category, slug=slug)
    if category is None:
        raise NotFound(f"Категория slug={slug} не существует")

    return category.get_children().filter(is_published=True)


def get_category_product_list(slug: str, filters: dict = None) -> QuerySet:
    filters = filters or {}

    category = get_object_or_None(Category, slug=slug)
    if category is None:
        raise NotFound(f"Категория slug={slug} не существует")
    qs = category.products.filter(is_published=True)

    first_property = category.product_properties.exclude(
        code__in=[
            "gost",
            "marka-stali",
            "poverkhnost",
            "occvet",
            "ves-metra",
            "ves-shtuki",
            "tolshina-stenki",
        ]
    ).first()
    if first_property:
        qs = qs.annotate(
            property_value=Cast(
                Subquery(
                    ProductPropertyValue.objects.filter(
                        property_id=first_property.id, product_id=OuterRef("pk")
                    ).values(
                        property_value=Func(
                            F("value"),
                            Value(","),
                            Value("."),
                            function="REPLACE",
                            output_field=CharField(),
                        )
                    )[
                        :1
                    ]
                ),
                output_field=FloatField(),
            )
        ).order_by("property_value")

    return ProductFilter(filters, qs).qs
