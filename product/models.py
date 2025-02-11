from django.db import models


class TimeStappedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStappedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    @property
    def is_on_discount(self):
        """Проверяет, находится ли продукт на скидке."""
        return self.discount > 0

    @property
    def discounted_price(self):
        """Возвращает цену с учетом скидки."""
        return float(self.price) * (1 - float(self.discount) / 100)