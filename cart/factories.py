import factory
from django.utils import timezone
from .models import Cart
from promocode.factories import PromoCodeFactory
from user.factories import ClientFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(ClientFactory)
    expires_at = factory.Faker("future_datetime", tzinfo=timezone.get_current_timezone())
    promo_code = factory.SubFactory(PromoCodeFactory)