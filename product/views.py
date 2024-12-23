from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from online_store_drf.permissions import IsClient, IsManager
from .models import Product
from .serializers import ProductSerializer, ProductDiscountSerializer


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


class SetProductDiscountView(APIView):
    """
    Эндпоинт для установки скидки на продукт.
    """
    permission_classes = [IsManager]
    
    def patch(self, request, pk):

        product = get_object_or_404(Product, pk=pk)

        serializer = ProductDiscountSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)