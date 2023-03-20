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
    # Переделать модели BaseModel и SEOModel используя django_extensions
    # Дописать сигналы
    slug = AutoSlugField(
        verbose_name="slug",
        editable=True,
        blank=False,
        populate_from="name",
        slugify_function=slugify,
    )
    seo_title = models.CharField(max_length=250, blank=True, verbose_name="SEO Title")
    seo_description = models.CharField(
        max_length=300, blank=True, verbose_name="SEO Description"
    )
    h1 = models.CharField(max_length=250, blank=True, verbose_name="H1")
    is_index = models.BooleanField(verbose_name="Robots index", default=True)
    is_follow = models.BooleanField(verbose_name="Robots follow", default=True)

    class Meta:
        abstract = True


class Category(BaseModel, SEOModel, MP_Node):
    name = models.CharField(verbose_name="Название категории", max_length=500)
    description = models.TextField(verbose_name="Описание", max_length=1500, blank=True)
    weight_coefficient = models.DecimalField(
        verbose_name="Коэфициент веса", max_digits=20, decimal_places=2, default=1.00
    )
    price_coefficient = models.DecimalField(
        verbose_name="Коэфициент цены", max_digits=20, decimal_places=2, default=1.00
    )

    node_order_by = ["name"]

    def __str__(self) -> str:
        return self.name

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


class Product(BaseModel, SEOModel):
    # images
    name = models.CharField(verbose_name="Название продукта", max_length=500)
    description = models.TextField(verbose_name="Описание", max_length=2500, blank=True)
    unit_price = models.DecimalField(
        verbose_name="Цена за штуку", max_digits=20, decimal_places=2, default=0.00
    )
    ton_price = models.DecimalField(
        verbose_name="Цена за тонну", max_digits=20, decimal_places=2, default=0.00
    )
    meter_price = models.DecimalField(
        verbose_name="Цена за метр", max_digits=20, decimal_places=2, default=0.00
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        null=True,
    )
    properties = models.ManyToManyField(
        ProductProperty,
        verbose_name="Свойства",
        related_name="products",
        through="ProductPropertyValue",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.category if self.category else 'Без категории'})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="properties_through"
    )
    property = models.ForeignKey(
        ProductProperty, on_delete=models.CASCADE, related_name="values"
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
