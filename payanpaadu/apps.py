from django.apps import AppConfig
from django.core.checks import register

from .checks import Tags, check_and_create_azure_container


class PayanpaaduConfig(AppConfig):
    name = 'payanpaadu'

    def ready(self):
        super(PayanpaaduConfig, self).ready()
        register(Tags.check_and_create_azure_container)(check_and_create_azure_container)
