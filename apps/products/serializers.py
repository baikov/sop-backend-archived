from rest_framework import serializers


class ProductFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=20, decimal_places=2)


class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
