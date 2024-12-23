from django.db import models
from django.utils import timezone
from user.models import ClientUser
from django.apps import apps

class Cart(models.Model):
    user = models.OneToOneField(ClientUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        if not self.id:
            super().save(*args, **kwargs)
            # Планируем задачу на момент expires_at
            clear_cart_task = apps.get_model('cart', 'clear_cart')
            clear_cart_task.apply_async(args=[self.id], eta=self.expires_at)
        else:
            super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Считает общую стоимость корзины."""
        return sum(item.total_price for item in self.cart_products.all())