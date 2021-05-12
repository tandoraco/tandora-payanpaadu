from django.apps import AppConfig


class PayanpaaduConfig(AppConfig):
    name = 'payanpaadu'

    def ready(self):
        super(PayanpaaduConfig, self).ready()
        # register(Tags.check_and_create_azure_container)(check_and_create_azure_container)
