from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from product.views import ProductViewSet
from cart.views import CartViewSet
from cart_product.views import CartProductViewSet
from user.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r"products", ProductViewSet)
router.register(r"carts", CartViewSet)
router.register(r"cart-products", CartProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
