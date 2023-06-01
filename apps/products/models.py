from functools import partial

from django.db import models
from django_extensions.db.models import (
    AutoSlugField,  # ActivatorModel, TimeStampedModel
)
from slugify import slugify
from treebeard.mp_tree import MP_Node


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)
    ordering = models.PositiveSmallIntegerField(verbose_name="Порядок", default=500)

    class Meta:
        abstract = True
        ordering = ("ordering",)


class SEOModel(models.Model):
    # TODO: Переделать модели BaseModel и SEOModel используя django_extensions
    # TODO: Дописать сигналы
    slug = AutoSlugField(
        verbose_name="slug",
        editable=True,
        blank=False,
        populate_from="name",
        slugify_function=partial(slugify, replacements=[["я", "ya"], ["/", ""]]),
        max_length=150,
    )
    seo_title = models.CharField(max_length=350, blank=True, verbose_name="SEO Title")
    seo_description = models.CharField(
        max_length=500, blank=True, verbose_name="SEO Description"
    )
    h1 = models.CharField(max_length=250, blank=True, verbose_name="H1")
    is_index = models.BooleanField(verbose_name="Robots index", default=True)
    is_follow = models.BooleanField(verbose_name="Robots follow", default=True)

    class Meta:
        abstract = True


class Category(BaseModel, SEOModel, MP_Node):
    parsed_name = models.CharField(
        verbose_name="Название категории из парсинга", max_length=500, blank=True
    )
    name = models.CharField(verbose_name="Название категории", max_length=500)
    description = models.TextField(verbose_name="Описание", max_length=1500, blank=True)
    parse_url = models.URLField(verbose_name="URL парсинга", blank=True, max_length=500)
    weight_coefficient = models.DecimalField(
        verbose_name="Коэфициент веса", max_digits=20, decimal_places=2, default=1.00
    )
    price_coefficient = models.DecimalField(
        verbose_name="Коэфициент цены", max_digits=20, decimal_places=2, default=1.00
    )
    last_parsed_at = models.DateTimeField(
        verbose_name="Дата последнего парсинга", blank=True, null=True
    )
    is_parsing_successful = models.BooleanField(
        verbose_name="Парсинг успешный", default=False
    )
    image = models.ImageField(
        verbose_name="Изображение", upload_to="categories/", blank=True
    )

    node_order_by = ["name"]

    def __str__(self) -> str:
        return self.name if self.name else self.parsed_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductProperty(BaseModel):
    name = models.CharField(verbose_name="Название свойства", max_length=250)
    code = AutoSlugField(
        verbose_name="Код свойства",
        editable=True,
        blank=False,
        populate_from="name",
        slugify_function=slugify,
    )
    description = models.CharField(verbose_name="Описание", max_length=2500, blank=True)
    categories = models.ManyToManyField(
        Category, verbose_name="Категории продуктов", related_name="product_properties"
    )
    units = models.CharField(
        verbose_name="Единицы измерения", max_length=250, blank=True
    )
    is_display_in_list = models.BooleanField(
        verbose_name="Отображать в списке продкутов?", default=False
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Свойство товара"
        verbose_name_plural = "Свойства товаров"
        ordering = ("ordering",)


class PropertyValue(models.Model):
    property = models.ForeignKey(
        ProductProperty,
        verbose_name="Свойство",
        related_name="values",
        on_delete=models.CASCADE,
    )
    value = models.CharField(verbose_name="Значение", max_length=250)

    def __str__(self):
        return f"{self.property.name}: {self.value}"


class Product(BaseModel, SEOModel):
    # images
    name = models.CharField(verbose_name="Название продукта", max_length=500)
    description = models.TextField(verbose_name="Описание", max_length=2500, blank=True)
    parse_url = models.URLField(verbose_name="URL парсинга", blank=True, max_length=500)
    unit_price = models.DecimalField(
        verbose_name="Цена за штуку", max_digits=20, decimal_places=2, default=0.00
    )
    ton_price = models.DecimalField(
        verbose_name="Цена за тонну", max_digits=20, decimal_places=2, default=0.00
    )
    meter_price = models.DecimalField(
        verbose_name="Цена за метр", max_digits=20, decimal_places=2, default=0.00
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name="Категории",
        related_name="products",
        through="ProductCategories",
    )
    properties = models.ManyToManyField(
        ProductProperty,
        verbose_name="Свойства",
        related_name="products",
        through="ProductPropertyValue",
    )
    in_stock = models.BooleanField(verbose_name="В наличии", default=True)

    def __str__(self) -> str:
        return self.name  # ({self.category if self.category else 'Без категории'})

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductCategories(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_categories"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_categories"
    )
    is_primary = models.BooleanField(verbose_name="Главная категория", default=False)
    is_display = models.BooleanField(
        verbose_name="Отображать в категории?", default=False
    )


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="properties_through"
    )
    property = models.ForeignKey(
        ProductProperty, on_delete=models.CASCADE, related_name="values_through"
    )
    value = models.CharField(verbose_name="Значение", max_length=250, blank=True)

    class Meta:
        unique_together = ("product", "property")
        verbose_name = "Значение свойства продукта"
        verbose_name_plural = "Значения свойств продукта"
        ordering = ("property__ordering",)


class Navigation(models.Model):
    name = models.CharField(verbose_name="Название меню", max_length=250)
    code = AutoSlugField(
        verbose_name="Код меню",
        editable=True,
        blank=False,
        populate_from="name",
        slugify_function=slugify,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class NavigationItem(MP_Node):
    name = models.CharField(verbose_name="Название пункта меню", max_length=250)
    url = models.CharField(verbose_name="Ссылка пункта меню", max_length=250)
    navigation = models.ForeignKey(
        Navigation, verbose_name="Меню", related_name="items", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
