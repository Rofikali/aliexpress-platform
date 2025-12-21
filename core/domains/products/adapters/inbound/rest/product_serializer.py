from rest_framework import serializers

class CreateProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    seller_id = serializers.UUIDField()
    title = serializers.CharField()
