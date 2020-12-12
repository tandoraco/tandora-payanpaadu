import os
from datetime import datetime

from dotenv import load_dotenv
from storages.backends.azure_storage import AzureStorage

STORAGE_LOCATION_FORMAT = f'user-uploads/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}'

load_dotenv()


class AzureMediaStorage(AzureStorage):
    account_name = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY')
    azure_container = os.environ.get('MEDIA_LOCATION')
    expiration_secs = None
    # location = STORAGE_LOCATION_FORMAT
