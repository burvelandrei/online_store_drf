import factory
from .models import CartProduct
from cart.factories import CartFactory
from product.factories import ProductFactory

class CartProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartProduct

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)