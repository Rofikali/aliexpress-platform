from rest_framework import serializers


class ProductSearchSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    price = serializers.FloatField()
    seller_id = serializers.UUIDField()
    status = serializers.CharField()
    occurred_at = serializers.DateTimeField()
