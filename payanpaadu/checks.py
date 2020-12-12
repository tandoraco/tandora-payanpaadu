import os

from azure.common import AzureMissingResourceHttpError
from azure.storage.blob import BlockBlobService
from django.conf import settings
from django.core.checks import Tags as DjangoTags, register


class Tags(DjangoTags):
    check_and_create_azure_container = 'check_and_create_azure_container'


@register(Tags.check_and_create_azure_container)
def check_and_create_azure_container(app_config=None, **kwargs):
    container_name = os.environ.get('MEDIA_LOCATION')

    if hasattr(settings, 'DEFAULT_FILE_STORAGE') and 'AzureMediaStorage' not in settings.DEFAULT_FILE_STORAGE:
        print('AzureMediaStorage is not configured in settings ..')
        print('Skipping container check ..')

    try:
        blob_client = BlockBlobService(account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
                                       account_key=settings.AZURE_STORAGE_ACCOUNT_KEY)

        blob_client.get_container_properties(container_name)
    except AzureMissingResourceHttpError:
        print('container does not exist .. ')
        print(f'creating container {container_name} ..')
        blob_client.create_container(container_name, public_access='blob')

    return []
