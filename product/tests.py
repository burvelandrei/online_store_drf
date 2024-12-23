from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import Product
from .factories import ProductFactory
from .views import ProductViewSet, SetProductDiscountView
from user.factories import ClientFactory, ManagerFactory


class ProductViewSetTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'partial_update', 'delete': 'destroy'})
        self.manager_user = ManagerFactory()
        self.regular_user = ClientFactory()
        self.product = ProductFactory()

    def test_list_products_allowed_for_anyone(self):
        """Проверяем, что список продуктов доступен для всех."""
        request = self.factory.get(reverse('product-list'))
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product_allowed_for_anyone(self):
        """Проверяем, что детали продукта доступны для всех."""
        request = self.factory.get(reverse('product-detail', args=[self.product.id]))
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.product.name)

    def test_create_product_allowed_for_manager(self):
        """Проверяем, что создание продукта доступно только для менеджера."""
        request = self.factory.post(reverse('product-list'), data={'name': 'New Product', 'price': 100})
        force_authenticate(request, user=self.manager_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_denied_for_regular_user(self):
        """Проверяем, что создание продукта недоступно для обычного пользователя."""
        request = self.factory.post(reverse('product-list'), data={'name': 'New Product', 'price': 100})
        force_authenticate(request, user=self.regular_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_allowed_for_manager(self):
        """Проверяем, что обновление продукта доступно только для менеджера."""
        request = self.factory.patch(reverse('product-detail', args=[self.product.id]), data={'price': 150})
        force_authenticate(request, user=self.manager_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 150)

    def test_update_product_denied_for_regular_user(self):
        """Проверяем, что обновление продукта недоступно для обычного пользователя."""
        request = self.factory.patch(reverse('product-detail', args=[self.product.id]), data={'price': 150})
        force_authenticate(request, user=self.regular_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_allowed_for_manager(self):
        """Проверяем, что удаление продукта доступно только для менеджера."""
        request = self.factory.delete(reverse('product-detail', args=[self.product.id]))
        force_authenticate(request, user=self.manager_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_product_denied_for_regular_user(self):
        """Проверяем, что удаление продукта недоступно для обычного пользователя."""
        request = self.factory.delete(reverse('product-detail', args=[self.product.id]))
        force_authenticate(request, user=self.regular_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SetProductDiscountViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SetProductDiscountView.as_view()
        self.manager_user = ManagerFactory()
        self.regular_user = ClientFactory()
        self.product = ProductFactory()

    def test_set_discount_allowed_for_manager(self):
        """Проверяем, что установка скидки доступна для менеджера."""
        request = self.factory.patch(reverse('set-product-discount', args=[self.product.id]), data={'discount': 10})
        force_authenticate(request, user=self.manager_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.discount, 10)

    def test_set_discount_denied_for_regular_user(self):
        """Проверяем, что установка скидки недоступна для обычного пользователя."""
        request = self.factory.patch(reverse('set-product-discount', args=[self.product.id]), data={'discount': 10})
        force_authenticate(request, user=self.regular_user)
        response = self.view(request, pk=self.product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)