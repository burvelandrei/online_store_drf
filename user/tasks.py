from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from user.models import ClientUser
from product.models import Product


@shared_task
def send_discount_newsletter():
    """
    Отправляет рассылку с информацией о скидках подписанным пользователям.
    """
    # Получаем всех подписанных пользователей
    subscribers = ClientUser.objects.filter(is_subscribed=True)

    # Получаем все продукты, находящиеся на скидке
    discounted_products = Product.objects.filter(is_on_discount=True)

    for subscriber in subscribers:
        # Отправляем письмо
        subject = "Актуальные скидки на нашем сайте!"
        message = render_to_string(
            "discount_newsletter.html",
            {
                "user": subscriber,
                "discounted_products": discounted_products,
            },
        )
        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.email],
            html_message=message,
        )
