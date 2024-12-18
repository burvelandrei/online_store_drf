from rest_framework import viewsets
from .models import CartProduct
from .serializers import CartProductSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
