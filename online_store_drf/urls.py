from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet
from cart.views import CartViewSet
from cart_product.views import CartProductViewSet


router = DefaultRouter()
# router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-products', CartProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
