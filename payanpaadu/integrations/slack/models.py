import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

SLACK_OAUTH_VALID_TIME_IN_MINUTES = 10


class SlackOAuthState(models.Model):
    company = models.ForeignKey(settings.COMPANY_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_callback_processed = models.DateTimeField(default=False)

    def is_valid(self):
        return timezone.now() < (self.created_at + timedelta(minutes=SLACK_OAUTH_VALID_TIME_IN_MINUTES))

    def __str__(self):
        return f'{self.uuid}'
