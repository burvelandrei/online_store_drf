from django.db import models
from .models import Cart, Product


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart}"

    @property
    def total_price(self):
        """Считает общую стоимость продукта в корзине с учетом скидки."""
        return self.product.discounted_price * self.quantity