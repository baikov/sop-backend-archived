from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.products.views import CategoryViewSet, ProductViewSet
from apps.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")


app_name = "api"
urlpatterns = router.urls
