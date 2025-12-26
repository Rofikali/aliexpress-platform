# file name: core/domains/products/adapters/inbound/rest/product_serializer.py
from rest_framework import serializers


class CreateProductSerializer(serializers.Serializer):
    # product_id = serializers.UUIDField()
    seller_id = serializers.UUIDField()
    title = serializers.CharField()
