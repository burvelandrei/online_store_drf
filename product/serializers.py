from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'discount', 'discounted_price']