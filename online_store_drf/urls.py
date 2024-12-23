from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, SetProductDiscountView
from cart.views import CartViewSet
from cart_product.views import CartProductViewSet
from user.views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    NewsletterSubscriptionView,
)
from cart.views import (
    AddProductToCartView,
    DecreaseProductQuantityView,
    DeleteCartView,
    RemoveProductFromCartView,
    ApplyPromoCodeView,
)


router = DefaultRouter()
router.register("api/product", ProductViewSet, "product")
router.register("api/cart", CartViewSet, "cart")
router.register("api/cart-products", CartProductViewSet, "cart_product")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/user/register/",
        UserRegisterView.as_view(),
        name="user_register",
    ),
    path(
        "api/user/login/",
        UserLoginView.as_view(),
        name="user_login",
    ),
    path(
        "api/user/logout/",
        UserLogoutView.as_view(),
        name="user_logout",
    ),
    path(
        "api/cart/add/<int:product_id>/",
        AddProductToCartView.as_view(),
        name="add-product-to-cart",
    ),
    path(
        "api/cart/decrease/<int:product_id>/",
        DecreaseProductQuantityView.as_view(),
        name="decrease-product-quantity",
    ),
    path(
        "api/cart/delete/",
        DeleteCartView.as_view(),
        name="delete-cart",
    ),
    path(
        "api/cart/remove/<int:product_id>/",
        RemoveProductFromCartView.as_view(),
        name="remove-product-from-cart",
    ),
    path(
        "api/cart/apply-promocode/",
        ApplyPromoCodeView.as_view(),
        name="apply-promocode",
    ),
    path(
        "api/newsletter/subscribe/",
        NewsletterSubscriptionView.as_view(),
        name="newsletter-subscribe",
    ),
    path(
        "api/product/<int:pk>/set-discount/",
        SetProductDiscountView.as_view(),
        name="set-product-discount",
    ),
] + router.urls
