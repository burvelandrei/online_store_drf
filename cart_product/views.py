from rest_framework import viewsets
from online_store_drf.permissions import IsClient
from .models import CartProduct
from .serializers import CartProductSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsClient]
