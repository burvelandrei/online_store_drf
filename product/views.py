from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from online_store_drf.permissions import IsClient, IsManager
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Возвращает разрешения в зависимости от типа действия.
        """
        if self.action in ['list', 'retrieve']:
            # Любой может просматривать товары
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Только менеджер может создавать, редактировать и удалять товары
            permission_classes = [IsManager]
        else:
            # По умолчанию разрешено только чтение
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]