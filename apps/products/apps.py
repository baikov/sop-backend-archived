from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = "apps.products"
    verbose_name = _("Products")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        try:
            import apps.products.signals  # noqa F401
        except ImportError:
            pass
