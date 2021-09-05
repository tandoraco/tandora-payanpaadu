from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail


def send_pending_signup_mail(sender, instance, created, **kwargs):
    if created:
        link = urljoin(settings.HOST, f'verify-signup/{instance.hash}')
        message_html = f'Click <a href="{link}">here</a> to verify y    our email and ' \
                       f'claim your free {settings.TANDORA_APP_NAME}' \
                       f'account. <br>' \
                       f'Alternatively, you can also copy paste the following link in a new tab to verify your email ' \
                       f'and claim your free account. <br> {link}'
        send_mail(
            subject=f'Claim your free account - {settings.TANDORA_APP_NAME}',
            message=message_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=message_html
        )
