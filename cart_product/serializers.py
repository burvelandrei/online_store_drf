from rest_framework import serializers
from .serializers import ProductSerializer
from .models import CartProduct, Product


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']