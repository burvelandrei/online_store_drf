from django.db import models
from django.utils import timezone
from user.models import ClientUser


class Cart(models.Model):
    user = models.OneToOneField(ClientUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.expires_at > timezone.now()

    @property
    def total_price(self):
        """Считает общую стоимость корзины."""
        return sum(item.total_price for item in self.cart_products.all())