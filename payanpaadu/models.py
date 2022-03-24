import uuid

from django.db import models

# Create your models here.
from django.db.models.signals import post_save

from payanpaadu.signup.signals import send_pending_signup_mail
from payanpaadu.multitenant.models import Instance
from payanpaadu.custom_domains.models import CustomDomain


def get_hash():
    return str(uuid.uuid4()).replace('-', '')


class PendingSignup(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=50, default=get_hash)

    def __str__(self):
        return self.email


post_save.connect(send_pending_signup_mail, sender=PendingSignup)
