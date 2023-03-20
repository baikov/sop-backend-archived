from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.products.models import (
    Category,
    Navigation,
    NavigationItem,
    Product,
    ProductProperty,
    ProductPropertyValue,
)


class PropertyInline(admin.TabularInline):
    model = ProductProperty.categories.through
    raw_id_fields = ["productproperty"]


class CategoryAdmin(TreeAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "is_published")
    list_editable = ("is_published",)
    # list_filter = ["region"]
    inlines = [PropertyInline]
    search_fields = ["name"]
    readonly_fields = ["updated_date", "created_date"]
    form = movenodeform_factory(Category)


class ProductPropertyInline(admin.TabularInline):
    model = ProductPropertyValue
    extra = 2
    fk_name = "product"
    raw_id_fields = ("property",)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "category",
        "slug",
        "ton_price",
        "unit_price",
        "meter_price",
        "cat_price_coefficient",
        "id",
        "is_published",
    )
    list_editable = ("is_published", "ton_price")
    list_filter = ["category"]
    inlines = [ProductPropertyInline]

    def cat_price_coefficient(self, obj):
        # sign = "+" if obj.category.price_coefficient - 1 > 0 else ""
        # return f"{sign}{int(obj.category.price_coefficient * 100 - 100)}%"
        return obj.category.price_coefficient

    cat_price_coefficient.short_description = "Коэфициент цены"


class ProductPropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"code": ("name",)}
    list_display = (
        "name",
        "code",
        "units",
        "ordering",
        "id",
        "is_display_in_list",
        "is_published",
    )
    list_editable = ("is_published", "units", "ordering", "is_display_in_list")
    list_filter = ["categories"]


class NavigationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
    )


class NavigationItemAdmin(TreeAdmin):
    list_display = (
        "name",
        "url",
    )
    list_filter = ["navigation"]
    list_editable = ("url",)
    search_fields = ["name"]
    form = movenodeform_factory(NavigationItem)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductProperty, ProductPropertyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(Navigation, NavigationAdmin)
