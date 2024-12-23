import factory
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    is_subscribed = factory.Faker("boolean")
    role = User.Role.CLIENT

class ManagerFactory(UserFactory):
    role = User.Role.MANAGER

class ClientFactory(UserFactory):
    role = User.Role.CLIENT