from django.db import models


# This model is to test the working of storage backend defined in payanpaadu app.
from payanpaadu.webhooks.models import Webhook, WebhookLog


class Profile(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    picture = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.name


class WebhookTest(Webhook):
    send_webhook = models.BooleanField(default=True)


class WebhookLogTest(WebhookLog):
    webhook = models.ForeignKey('WebhookTest', on_delete=models.CASCADE)
