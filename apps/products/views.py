from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.products.models import Category, Product
from apps.products.pagination import LimitOffsetPagination, get_paginated_response
from apps.products.serializers import (
    CatalogLeftMenuSerializer,
    CategoryDetailOutputSerializer,
    CategoryListOutputSerializer,
    ProductDetailOutputSerializer,
    ProductFilterSerializer,
    ProductListOutputSerializer,
)
from apps.products.services.categories import (
    get_category_list,
    get_category_product_list,
    get_children_categories,
    get_root_categories,
)
from apps.products.services.products import get_products_list
from apps.utils.custom import get_object_or_None


class ProductViewSet(ViewSet):
    lookup_field = "slug"

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
        data = ProductListOutputSerializer(products, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        qs = Product.objects.select_related("category").prefetch_related(
            "properties_through__property"
        )
        product = get_object_or_None(qs, slug=slug)
        data = ProductDetailOutputSerializer(product).data
        return Response(data)


class CategoryViewSet(ViewSet):
    lookup_field = "slug"

    class Pagination(LimitOffsetPagination):
        default_limit = 20

    def get_permissions(self):
        if self.action in ("list", "retrieve", "products", "children", "root", "menu"):
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAdminUser,
            ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        categories = get_category_list()
        data = CategoryListOutputSerializer(categories, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        category = get_object_or_None(Category, slug=slug)
        data = CategoryDetailOutputSerializer(category).data
        return Response(data)

    @action(methods=["GET"], detail=False)
    def root(self, request):
        root_categories = get_root_categories()
        data = CategoryListOutputSerializer(root_categories, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def children(self, request, slug=None):
        children_categories = get_children_categories(slug=slug)
        data = CategoryListOutputSerializer(children_categories, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def products(self, request, slug=None):
        filters_serializer = ProductFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        products = get_category_product_list(
            slug=slug, filters=filters_serializer.validated_data
        )
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=ProductListOutputSerializer,
            queryset=products,
            request=request,
            view=self,
        )

    @action(methods=["GET"], detail=False)
    def menu(self, request):
        items = get_root_categories().filter(is_published=True)
        data = CatalogLeftMenuSerializer(items, many=True).data

        return Response(data, status=status.HTTP_200_OK)


# class NavigationViewSet(ViewSet):
#     # lookup_field = "code"

#     def get_permissions(self):
#         if self.action in ("retrieve"):
#             permission_classes = [
#                 AllowAny,
#             ]
#         else:
#             permission_classes = [
#                 IsAdminUser,
#             ]
#         return [permission() for permission in permission_classes]

#     def retrieve(self, request, pk=None):
#         # qs = NavigationItem.objects.filter(navigation_id=pk)
#         nav = get_object_or_None(Navigation, pk=pk)
#         data = NavigationDetailOutputSerializer(nav).data
#         return Response(data)
