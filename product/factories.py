import factory
from .models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    description = factory.Faker("text", max_nb_chars=200)
    discount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True, max_value=100)