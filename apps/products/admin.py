from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.products.models import (
    Category,
    Navigation,
    NavigationItem,
    Product,
    ProductCategories,
    ProductProperty,
    ProductPropertyValue,
    PropertyValue,
)


class PropertyInline(admin.TabularInline):
    model = ProductProperty.categories.through
    raw_id_fields = ["productproperty"]


class CategoryAdmin(TreeAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "cat_name",
        "slug",
        "is_published",
        "is_parsing_successful",
        "id",
    )
    list_editable = ("is_published",)
    list_filter = ["is_published"]
    inlines = [PropertyInline]
    search_fields = ["parsed_name", "name"]
    readonly_fields = ["updated_date", "created_date", "parse_url"]
    form = movenodeform_factory(Category)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "description",
                    "weight_coefficient",
                    "price_coefficient",
                    "is_published",
                    "_position",
                    "_ref_node_id",
                ],
            },
        ),
        (
            "Парсинг",
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "parsed_name",
                    "parse_url",
                    "last_parsed_at",
                    "is_parsing_successful",
                ],
            },
        ),
        (
            "SEO",
            {
                "classes": ("collapse", "wide"),
                "fields": [
                    "slug",
                    "seo_title",
                    "seo_description",
                    "h1",
                    "is_index",
                    "is_follow",
                    "ordering",
                ],
            },
        ),
    ]

    def cat_name(self, obj):
        return obj.name if obj.name else obj.parsed_name

    cat_name.short_description = "Название категории"


class ProductPropertyInline(admin.TabularInline):
    model = ProductPropertyValue
    extra = 2
    fk_name = "product"
    raw_id_fields = ("property",)


class ProductCategoriesInline(admin.TabularInline):
    model = ProductCategories
    extra = 2
    fk_name = "product"
    raw_id_fields = ("category",)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        # "category",
        "slug",
        "ton_price",
        "unit_price",
        "meter_price",
        # "cat_price_coefficient",
        "id",
        "in_stock",
        "is_published",
        # "prop_values_list",
    )
    # exclude = ["prop_values"]
    list_editable = ("is_published", "ton_price")
    list_filter = ["categories", "in_stock"]
    search_fields = ["name"]
    inlines = [ProductPropertyInline, ProductCategoriesInline]
    readonly_fields = ["updated_date", "created_date"]
    # inlines = [ProductCategoriesInline, PropertyValueInline]

    # def cat_price_coefficient(self, obj):
    #     # sign = "+" if obj.category.price_coefficient - 1 > 0 else ""
    #     # return f"{sign}{int(obj.category.price_coefficient * 100 - 100)}%"
    #     return obj.category.price_coefficient

    # cat_price_coefficient.short_description = "Коэфициент цены"

    # def prop_values_list(self, obj):
    #     return ", ".join([p.value for p in obj.prop_values.all()])

    # prop_values_list.short_description = "Значения свойств"


@admin.register(PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ("property", "value")


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
