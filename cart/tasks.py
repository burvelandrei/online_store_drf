from celery import shared_task
from django.apps import apps

@shared_task
def clear_cart(cart_id):
    """
    Удаляет корзину по её ID.
    """
    Cart = apps.get_model('cart', 'Cart')  
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        print(f"Корзина {cart_id} удалена.")
    except Cart.DoesNotExist:
        print(f"Корзина {cart_id} не найдена.")