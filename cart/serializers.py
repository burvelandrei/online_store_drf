from rest_framework import serializers
from .serializers import CartProductSerializer
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'expires_at', 'cart_products', 'total_price']