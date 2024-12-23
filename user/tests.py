from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, ClientUser, Manage
from .factories import UserFactory, ManagerFactory, ClientFactory

class UserModelTests(TestCase):
    def test_user_creation(self):
        """Проверяем, что пользователь создается корректно."""
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertEqual(user.role, User.Role.CLIENT)
        self.assertTrue(user.check_password("password"))

    def test_manager_creation(self):
        """Проверяем, что менеджер создается корректно."""
        manager = ManagerFactory()
        self.assertIsInstance(manager, User)
        self.assertEqual(manager.role, User.Role.MANAGER)
        self.assertTrue(manager.is_manager)
        self.assertFalse(manager.is_client)

    def test_client_creation(self):
        """Проверяем, что клиент создается корректно."""
        client = ClientFactory()
        self.assertIsInstance(client, User)
        self.assertEqual(client.role, User.Role.CLIENT)
        self.assertTrue(client.is_client)
        self.assertFalse(client.is_manager)

    def test_save_method_with_is_staff(self):
        """Проверяем, что метод save корректно устанавливает роль менеджера."""
        user = UserFactory(is_staff=True)
        self.assertEqual(user.role, User.Role.MANAGER)
        self.assertTrue(user.is_manager)

    def test_client_manager(self):
        """Проверяем, что ClientManager возвращает только клиентов."""
        ClientFactory.create_batch(3)
        ManagerFactory.create_batch(2)
        clients = ClientUser.objects.all()
        self.assertEqual(clients.count(), 3)
        for client in clients:
            self.assertEqual(client.role, User.Role.CLIENT)

    def test_manage_manager(self):
        """Проверяем, что ManageManager возвращает только менеджеров."""
        ClientFactory.create_batch(3)
        ManagerFactory.create_batch(2)
        managers = Manage.objects.all()
        self.assertEqual(managers.count(), 2)
        for manager in managers:
            self.assertEqual(manager.role, User.Role.MANAGER)

    def test_is_client_property(self):
        """Проверяем, что свойство is_client работает корректно."""
        client = ClientFactory()
        self.assertTrue(client.is_client)
        self.assertFalse(client.is_manager)

    def test_is_manager_property(self):
        """Проверяем, что свойство is_manager работает корректно."""
        manager = ManagerFactory()
        self.assertTrue(manager.is_manager)
        self.assertFalse(manager.is_client)


class UserLogoutViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user_logout')

    def test_user_logout(self):
        """Проверяем, что пользователь может выйти из системы."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "logout")


class UserLoginViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user_login')

    def test_user_login_success(self):
        """Проверяем, что пользователь может войти в систему."""
        data = {
            'username': self.user.username,
            'password': 'password',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class UserRegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('user_register')

    def test_user_registration_success(self):
        """Проверяем, что пользователь может зарегистрироваться."""
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'password1':'newpassword',
            'first_name': 'new',
            'last_name': 'user',
            'email': 'newuser@example.com',
            'phone_number': '+375298887766',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully")
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_invalid_data(self):
        """Проверяем, что регистрация с неверными данными завершается ошибкой."""
        data = {
            'username': '',
            'password': 'newpassword',
            'email': 'invalid_email',
            'phone_number': 'invalid_phone',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NewsletterSubscriptionViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_subscribed=False)
        self.url = reverse('newsletter-subscribe')

    def test_subscribe_to_newsletter(self):
        """Проверяем, что пользователь может подписаться на рассылку."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You have successfully subscribed to the newsletter")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_subscribed)

    def test_unsubscribe_from_newsletter(self):
        """Проверяем, что пользователь может отписаться от рассылки."""
        self.user.is_subscribed = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You have unsubscribed from the mailing list")
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_subscribed)

    def test_unauthenticated_user_cannot_subscribe(self):
        """Проверяем, что неавторизованный пользователь не может подписаться."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_unsubscribe(self):
        """Проверяем, что неавторизованный пользователь не может отписаться."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)