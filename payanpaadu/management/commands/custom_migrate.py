from django.conf import settings
from django.core.management import BaseCommand, call_command

from payanpaadu.logger import get_logger
from payanpaadu.multitenant.models import Instance


class Command(BaseCommand):
    logger = get_logger()

    def _run_migration(self, database, instance):
        if database not in settings.DATABASES:
            settings.DATABASES[database] = instance.database_config

        self.logger.info(f'[custom_migrate] running migration for database {database}')

        call_command('migrate', f'--database={database}')

    def add_arguments(self, parser):
        parser.add_argument('-d', '--database', type=str, help='Database to use for current migration')

    def handle(self, *args, **options):
        if not hasattr(settings, 'MULTI_TENANT_MODE'):
            raise RuntimeError('Can only be run on projects with multitenancy.')

        database = options.get('database')
        if not database:
            self.logger.info('No database specified. Running migration on all available databases.')

        if not database:
            instances = Instance.objects.all()
            for instance in instances:
                self._run_migration(instance.db_name, instance)
        else:
            instance = Instance.objects.get(db_name=database)
            self._run_migration(database, instance)
