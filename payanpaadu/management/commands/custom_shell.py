from django.conf import settings
from django.core.management import BaseCommand, call_command

from payanpaadu.multitenant.models import Instance
from payanpaadu.multitenant.thread import set_current_database


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d', '--database', type=str, help='Database to use for current shell')

    def handle(self, *args, **options):
        if not hasattr(settings, 'MULTI_TENANT_MODE'):
            raise RuntimeError('Can only be run on projects with multitenancy.')

        database = options.get('database')
        if not database:
            raise AssertionError('Database should be specified.')

        try:
            instance = Instance.objects.get(db_name=database)
        except Instance.DoesNotExist:
            self.stderr.write("Specified database does not exist ..")
        else:
            settings.DATABASES[instance.db_name] = instance.database_config
            set_current_database(instance.db_name)
            call_command('shell')
