from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from .models import Cart
from cart_product.models import CartProduct
from product.models import Product
from .factories import CartFactory
from cart_product.factories import CartProductFactory
from promocode.factories import PromoCodeFactory
from product.factories import ProductFactory
from user.factories import ClientFactory
from cart.factories import CartFactory
from cart_product.factories import CartProductFactory



class CartModelTests(TestCase):
    def setUp(self):
        self.cart = CartFactory()
        self.cart_product = CartProductFactory(cart=self.cart)
        self.promo_code = PromoCodeFactory(discount_percentage=20, is_cumulative=False)

    def test_cart_creation(self):
        """Проверяем, что объект Cart создается корректно."""
        self.assertIsInstance(self.cart, Cart)
        self.assertIsNotNone(self.cart.user)
        self.assertIsNotNone(self.cart.expires_at)
        self.assertGreater(self.cart.expires_at, timezone.now())

    def test_total_price_without_promo_code(self):
        """Проверяем, что total_price считается корректно без промокода."""
        total_price = self.cart.total_price
        expected_total_price = sum(
            item.total_price for item in self.cart.cart_products.all()
        )
        self.assertEqual(total_price, expected_total_price)

    def test_total_price_with_promo_code(self):
        """Проверяем, что total_price считается корректно с промокодом."""
        self.cart.promo_code = self.promo_code
        self.cart.save()

        total_price = self.cart.total_price
        total_with_discount = sum(
            item.total_price
            for item in self.cart.cart_products.filter(product__discount__gt=0)
        )
        total_without_discount = sum(
            item.total_price
            for item in self.cart.cart_products.exclude(product__discount__gt=0)
        )
        expected_total_price = self.promo_code.apply_discount(total_without_discount)

        self.assertEqual(total_price, expected_total_price + total_with_discount)

    def test_apply_promo_code_success(self):
        """Проверяем, что промокод применяется успешно."""
        promo_code_code = self.promo_code.code
        result = self.cart.apply_promo_code(promo_code_code)
        self.assertTrue(result)
        self.assertEqual(self.cart.promo_code, self.promo_code)

    def test_apply_promo_code_invalid(self):
        """Проверяем, что невалидный промокод не применяется."""
        invalid_promo_code = "INVALID_PROMO_CODE"
        result = self.cart.apply_promo_code(invalid_promo_code)
        self.assertFalse(result)

    def test_apply_promo_code_expired(self):
        """Проверяем, что просроченный промокод не применяется."""
        expired_promo_code = PromoCodeFactory(
            valid_from=timezone.now() - timezone.timedelta(days=2),
            valid_to=timezone.now() - timezone.timedelta(days=1),
        )
        result = self.cart.apply_promo_code(expired_promo_code.code)
        self.assertFalse(result)

    def test_total_price_with_cumulative_promo_code(self):
        """Проверяем, что total_price считается корректно с кумулятивным промокодом."""
        cumulative_promo_code = PromoCodeFactory(
            discount_percentage=10, is_cumulative=True
        )
        self.cart.promo_code = cumulative_promo_code
        self.cart.save()

        total_price = self.cart.total_price
        total_without_discount = sum(
            item.total_price for item in self.cart.cart_products.all()
        )
        expected_total_price = cumulative_promo_code.apply_discount(
            total_without_discount
        )

        self.assertEqual(total_price, expected_total_price)

class AddProductToCartViewTests(APITestCase):
    def setUp(self):
        self.user = ClientFactory()
        self.product = ProductFactory()
        self.cart = CartFactory(user=self.user)
        self.url = reverse('add-product-to-cart', args=[self.product.id])

    def test_add_product_to_cart(self):
        """Проверяем, что продукт добавляется в корзину."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartProduct.objects.count(), 1)
        self.assertEqual(CartProduct.objects.first().quantity, 1)

    def test_increase_product_quantity(self):
        """Проверяем, что количество продукта увеличивается."""
        CartProductFactory(cart=self.cart, product=self.product, quantity=1)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartProduct.objects.first().quantity, 2)

    def test_product_not_found(self):
        """Проверяем, что ошибка возвращается, если продукт не найден."""
        invalid_url = reverse('add-product-to-cart', args=[999])
        self.client.force_authenticate(user=self.user)
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Product not found")


class DecreaseProductQuantityViewTests(APITestCase):
    def setUp(self):
        self.user = ClientFactory()
        self.product = ProductFactory()
        self.cart = CartFactory(user=self.user)
        self.cart_product = CartProductFactory(cart=self.cart, product=self.product, quantity=2)
        self.url = reverse('decrease-product-quantity', args=[self.product.id])

    def test_decrease_product_quantity(self):
        """Проверяем, что количество продукта уменьшается."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartProduct.objects.first().quantity, 1)

    def test_remove_product_from_cart(self):
        """Проверяем, что продукт удаляется, если количество равно 1."""
        self.cart_product.quantity = 1
        self.cart_product.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartProduct.objects.count(), 0)

    def test_product_not_found_in_cart(self):
        """Проверяем, что ошибка возвращается, если продукт не найден в корзине."""
        invalid_url = reverse('decrease-product-quantity', args=[999])
        self.client.force_authenticate(user=self.user)
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Product not found in cart")


class RemoveProductFromCartViewTests(APITestCase):
    def setUp(self):
        self.user = ClientFactory()
        self.product = ProductFactory()
        self.cart = CartFactory(user=self.user)
        self.cart_product = CartProductFactory(cart=self.cart, product=self.product)
        self.url = reverse('remove-product-from-cart', args=[self.product.id])

    def test_remove_product_from_cart(self):
        """Проверяем, что продукт удаляется из корзины."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartProduct.objects.count(), 0)

    def test_product_not_found_in_cart(self):
        """Проверяем, что ошибка возвращается, если продукт не найден в корзине."""
        invalid_url = reverse('remove-product-from-cart', args=[999])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Product not found in cart")


class DeleteCartViewTests(APITestCase):
    def setUp(self):
        self.user = ClientFactory()
        self.cart = CartFactory(user=self.user)
        self.url = reverse('delete-cart')

    def test_delete_cart(self):
        """Проверяем, что корзина удаляется."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.count(), 0)

    def test_cart_not_found(self):
        """Проверяем, что ошибка возвращается, если корзина не найдена."""
        self.cart.delete()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Cart not found")


class ApplyPromoCodeViewTests(APITestCase):
    def setUp(self):
        self.user = ClientFactory()
        self.cart = CartFactory(user=self.user)
        self.promo_code = PromoCodeFactory(code="TESTCODE", discount_percentage=10)
        self.url = reverse('apply-promocode')

    def test_apply_promo_code_success(self):
        """Проверяем, что промокод применяется успешно."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={'promo_code': self.promo_code.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Promo code successfully applied")
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.promo_code, self.promo_code)

    def test_apply_promo_code_invalid(self):
        """Проверяем, что ошибка возвращается, если промокод невалидный."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={'promo_code': "INVALID_CODE"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Invalid or inactive promotional code")

    def test_cart_not_found(self):
        """Проверяем, что ошибка возвращается, если корзина не найдена."""
        self.cart.delete()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data={'promo_code': self.promo_code.code})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Cart not found")