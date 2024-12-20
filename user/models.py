from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = "manager"
        CLIENT = "client"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = self.Role.MANAGER
        super().save(*args, **kwargs)

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER


class ClientManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.CLIENT)


class ClientUser(User):
    class Meta:
        proxy = True

    objects = ClientManager()


class ManageManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.MANAGER)


class Manage(User):
    class Meta:
        proxy = True

    objects = ManageManager()
