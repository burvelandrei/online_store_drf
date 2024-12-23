from django.db import models


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_cumulative = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid(self):
        """Проверяет, активен ли промокод."""
        from django.utils import timezone
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def apply_discount(self, total_price):
        """Применяет скидку к общей сумме."""
        return total_price * (100 - self.discount_percentage) / 100

    def __str__(self):
        return self.code