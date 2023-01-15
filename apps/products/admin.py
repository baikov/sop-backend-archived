from django.contrib import admin

from apps.products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


admin.site.register(Product, ProductAdmin)
