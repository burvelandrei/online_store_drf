from django.db import models
from django.utils import timezone
from user.models import ClientUser
from django.apps import apps
from promocode.models import PromoCode
from .tasks import clear_cart

class Cart(models.Model):
    user = models.OneToOneField(ClientUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        if not self.id:
            super().save(*args, **kwargs)
            # Планируем задачу на момент expires_at
            clear_cart.apply_async(args=[self.id], eta=self.expires_at)
        else:
            super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Считает общую стоимость корзины."""
        total = sum(item.total_price for item in self.cart_products.all())
        total_with_discount_price = sum(
            item.total_price
            for item in self.cart_products.filter(product__discount__gt=0)
        )
        total_without_discount_price = sum(
            item.total_price
            for item in self.cart_products.exclude(product__discount__gt=0))

        # Применяем промокод
        if self.promo_code and self.promo_code.is_valid():
            if self.promo_code.is_cumulative:
                total = self.promo_code.apply_discount(total)
            else:
                total = self.promo_code.apply_discount(total_without_discount_price) + total_with_discount_price
        return total

    def apply_promo_code(self, promo_code):
        """Применяет промокод к корзине."""
        try:
            promo_code_obj = PromoCode.objects.get(code=promo_code)
            if promo_code_obj.is_valid():
                self.promo_code = promo_code_obj
                self.save()
                return True
            else:
                return False
        except PromoCode.DoesNotExist:
            return False