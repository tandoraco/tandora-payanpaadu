from django.db import models

from payanpaadu.utils import get_key


class Webhook(models.Model):
    active = models.BooleanField(default=False)
    key = models.CharField(max_length=32, default=get_key)
    name = models.CharField(max_length=20)
    url = models.URLField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class WebhookLog(models.Model):
    payload = models.TextField(default='{}')
    status_code = models.IntegerField()
    response = models.TextField(default='{}')
    trigger_time = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=32)

    class Meta:
        abstract = True
