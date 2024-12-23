from django.test import TestCase
from django.utils import timezone
from .factories import PromoCodeFactory

class PromoCodeFactoryTests(TestCase):
    def test_promo_code_factory(self):
        # Создаем промокод с помощью фабрики
        promo_code = PromoCodeFactory()

        # Проверяем, что объект создан
        self.assertIsNotNone(promo_code)

        # Проверяем, что поля заполнены корректно
        self.assertTrue(promo_code.code.startswith("PROMOCODE"))  
        self.assertGreaterEqual(promo_code.discount_percentage, 1)
        self.assertLessEqual(promo_code.discount_percentage, 100)
        self.assertIsInstance(promo_code.is_cumulative, bool)
        self.assertLess(promo_code.valid_from, promo_code.valid_to)
        self.assertLess(promo_code.valid_from, timezone.now())
        self.assertGreater(promo_code.valid_to, timezone.now())

    def test_promo_code_factory_with_custom_values(self):
        # Создаем промокод с пользовательскими значениями
        promo_code = PromoCodeFactory(
            code="CUSTOMCODE",
            discount_percentage=50,
            is_cumulative=True,
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
        )

        # Проверяем, что пользовательские значения сохранены корректно
        self.assertEqual(promo_code.code, "CUSTOMCODE")
        self.assertEqual(promo_code.discount_percentage, 50)
        self.assertTrue(promo_code.is_cumulative)
        self.assertEqual(promo_code.valid_from, timezone.now() - timezone.timedelta(days=1))
        self.assertEqual(promo_code.valid_to, timezone.now() + timezone.timedelta(days=1))