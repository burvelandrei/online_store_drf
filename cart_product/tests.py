from django.test import TestCase
from .models import CartProduct
from .factories import CartProductFactory, ProductFactory

class CartProductModelTests(TestCase):
    def test_cart_product_creation(self):
        """Проверяем, что объект CartProduct создается корректно."""
        cart_product = CartProductFactory()
        self.assertIsInstance(cart_product, CartProduct)
        self.assertGreater(cart_product.quantity, 0)
        self.assertIsNotNone(cart_product.cart)
        self.assertIsNotNone(cart_product.product)

    def test_total_price_property(self):
        """Проверяем, что свойство total_price считается корректно."""
        product = ProductFactory(price=100, discount=20)
        cart_product = CartProductFactory(product=product, quantity=3)

        expected_total_price = product.discounted_price * cart_product.quantity

        self.assertEqual(cart_product.total_price, expected_total_price)