from pathlib import Path

import boto3
from django.conf import settings
from django.core.management import BaseCommand

container_name = 'tandora-packages'
BLOB_PATH = f'https://{container_name}.s3.amazonaws.com/file_name'


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
        with open('current_payanpaadu_aws_url.txt', 'w') as f:
            f.write(url)
        print(url)

    def handle(self, *args, **options):
        session = boto3.Session(aws_access_key_id=settings.S3_AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.S3_AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.meta.client.upload_file(Filename=self.full_path_to_file.__str__(), Bucket=container_name,
                                   Key=self.local_file_name)

        object_acl = s3.ObjectAcl(container_name, self.local_file_name)
        response = object_acl.put(ACL='public-read')
        print(response)

        print(BLOB_PATH.replace('file_name', self.local_file_name))
