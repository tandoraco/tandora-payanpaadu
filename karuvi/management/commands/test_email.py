from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        html = '''
        html message
        <b>Hello world</b>
        <h1>h1</h1>
        <h2>h2</h2>
        <h3>h3</h3>
        <h4>h4</h4>
        '''
        message = 'Test plain text'
        send_mail(
            subject='Hello from tandora',
            message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['admin@tandora.co'],
            html_message=html
        )
