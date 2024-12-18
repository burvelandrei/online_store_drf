from django.db import models
from django.utils import timezone
from .models import CustomUser


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField()

    @property
    def is_active(self):
        return self.expires_at > timezone.now()

    @property
    def total_price(self):
        """Считает общую стоимость корзины."""
        return sum(item.total_price for item in self.cart_products.all())