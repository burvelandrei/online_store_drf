import factory
from django.utils import timezone
from .models import PromoCode

class PromoCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromoCode

    code = factory.Sequence(lambda n: f"PROMOCODE{n}")
    discount_percentage = factory.Faker("random_int", min=1, max=100)
    is_cumulative = factory.Faker("boolean")
    valid_from = factory.Faker("past_datetime", tzinfo=timezone.get_current_timezone())
    valid_to = factory.Faker("future_datetime", tzinfo=timezone.get_current_timezone())