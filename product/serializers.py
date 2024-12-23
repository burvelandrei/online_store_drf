from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'discount', 'discounted_price']


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['discount']

    def validate_discount(self, value):
        """
        Проверяем, что скидка находится в допустимом диапазоне (0-100).
        """
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Скидка должна быть в диапазоне от 0 до 100.")
        return value