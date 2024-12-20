from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CartProduct
from .serializers import CartProductSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]
