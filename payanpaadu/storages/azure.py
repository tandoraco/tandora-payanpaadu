from django.conf import settings


class AzureMediaStorage:
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.MEDIA_LOCATION
    expiration_secs = None
