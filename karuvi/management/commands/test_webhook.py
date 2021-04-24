import requests
from django.core.management import BaseCommand
from django.forms import model_to_dict

from karuvi.models import WebhookTest, WebhookLogTest
from payanpaadu.utils import get_key


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://webhook.site/c798d71a-0833-4118-9b4b-4f340083ba01'
        webhook = WebhookTest.objects.create(active=True, name='test', url=url)

        print(model_to_dict(webhook))

        payload = {'test': True}
        _hash = get_key()
        response = requests.post(url=url, data=payload, headers={'TANDORA_HASH': _hash})
        log = WebhookLogTest.objects.create(webhook=webhook, payload=payload, hash=_hash,
                                            status_code=response.status_code,
                                            response=response.content.decode())
        print(model_to_dict(log))
