from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.products.models import Product
from apps.products.serializers import ProductFilterSerializer, ProductOutputSerializer
from apps.products.services.products import get_products_list
from apps.utils.custom import get_object_or_None


class ProductViewSet(ViewSet):
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAdminUser,
            ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        filters_serializer = ProductFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        products = get_products_list(filters=filters_serializer.validated_data)
        data = ProductOutputSerializer(products, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = get_object_or_None(Product, pk=pk)
        data = ProductOutputSerializer(product).data
        return Response(data)
