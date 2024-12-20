from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from product.views import ProductViewSet
from cart.views import CartViewSet
from cart_product.views import CartProductViewSet
from user.views import UserRegisterView, UserLoginView, UserLogoutView


router = DefaultRouter()
router.register("api/product", ProductViewSet, 'product')
router.register("api/cart", CartViewSet, 'cart')
router.register("api/cart-products", CartProductViewSet, 'cart_product')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', UserRegisterView.as_view(), name='user_register'),
    path('api/user/login/', UserLoginView.as_view(), name='user_login'),
    path('api/user/logout/', UserLogoutView.as_view(), name='user_logout'),
] + router.urls
