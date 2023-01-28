from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.products.views import ProductViewSet
from apps.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet, basename="products")


app_name = "api"
urlpatterns = router.urls
