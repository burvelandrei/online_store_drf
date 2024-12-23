from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer
from cart_product.models import CartProduct
from cart_product.serializers import CartProductSerializer
from product.models import Product
from online_store_drf.permissions import IsClient


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsClient]


class AddProductToCartView(APIView):
    """
    Эднпоинт для добавления(увеличивает количество) продукта в корзину
    """
    permission_classes = [IsClient]

    def post(self, request, product_id):
        try:
            # Получаем продукт по ID
            product = Product.objects.get(id=product_id)

            # Получаем или создаем корзину для текущего пользователя
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Проверяем, есть ли уже такой продукт в корзине
            cart_product, created = CartProduct.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 1}
            )

            if not created:
                # Если продукт уже есть в корзине, увеличиваем количество
                cart_product.quantity += 1
                cart_product.save()

            # Сериализуем обновленный объект CartProduct
            serializer = CartProductSerializer(cart_product)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class DecreaseProductQuantityView(APIView):
    """
    Эднпоинт для уменьшения продукта в корзине
    """
    permission_classes = [IsClient]

    def post(self, request, product_id):
        try:
            # Получаем корзину текущего пользователя
            cart = Cart.objects.get(user=request.user)

            # Получаем продукт в корзине
            cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)

            # Уменьшаем количество
            if cart_product.quantity > 1:
                cart_product.quantity -= 1
                cart_product.save()
            else:
                # Если количество равно 1, удаляем продукт из корзины
                cart_product.delete()

            # Сериализуем обновленную корзину
            serializer = CartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CartProduct.DoesNotExist:
            return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


class RemoveProductFromCartView(APIView):
    """
    Эднпоинт для удаления продукта из корзины
    """
    permission_classes = [IsClient]

    def delete(self, request, product_id):
        try:
            # Получаем корзину текущего пользователя
            cart = Cart.objects.get(user=request.user)

            # Получаем продукт в корзине
            cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)

            # Удаляем продукт из корзины
            cart_product.delete()

            # Сериализуем обновленную корзину
            serializer = CartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CartProduct.DoesNotExist:
            return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteCartView(APIView):
    """
    Эднпоинт для удаления корзины
    """
    permission_classes = [IsClient]

    def delete(self, request):
        try:
            # Получаем корзину текущего пользователя
            cart = Cart.objects.get(user=request.user)

            # Удаляем корзину
            cart.delete()

            return Response({"message": "Cart bin successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)