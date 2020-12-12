from pathlib import Path

from azure.common import AzureMissingResourceHttpError
from azure.storage.blob import BlockBlobService
from django.core.management import BaseCommand

from django.conf import settings

container_name = 'packages'
BLOB_PATH = f'https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/file_name'


class Command(BaseCommand):

    @property
    def local_file_name(self):
        version = ''
        with open('version.txt') as version_file:
            version = version_file.read().strip()

        return f'tandora-payanpaadu-{version}.tar.gz'

    @property
    def full_path_to_file(self):
        return Path(settings.BASE_DIR) / Path('dist') / Path(self.local_file_name)

    def _update_current_url(self, url):
        with open('current_payanpaadu_azure_url.txt', 'w') as f:
            f.write(url)
        print(url)

    def handle(self, *args, **options):
        try:
            print('starting upload ..')
            blob_client = BlockBlobService(account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
                                           account_key=settings.AZURE_STORAGE_ACCOUNT_KEY)

            blob_client.get_container_properties(container_name)
        except AzureMissingResourceHttpError:
            print('container does not exist .. ')
            print(f'creating container {container_name} ..')
            blob_client.create_container(container_name, public_access='blob')
        finally:
            blob_client.create_blob_from_path(
                container_name, self.local_file_name, self.full_path_to_file.__str__())
            print('successfully uploaded ..')
            self._update_current_url(BLOB_PATH.replace('file_name', self.local_file_name))
