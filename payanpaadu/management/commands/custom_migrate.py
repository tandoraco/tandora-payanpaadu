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

    def handle(self, *args, **options):
        if not hasattr(settings, 'MULTI_TENANT_MODE'):
            raise RuntimeError('Can only be run on projects with multitenancy.')

        if settings.MULTI_TENANT_MODE:
            instances = Instance.objects.all()
            for instance in instances:
                self._run_migration(instance.db_name, instance)
        else:
            database = settings.INSTANCE_DATABASE_NAME
            instance = Instance.objects.get(db_name=database)
            self._run_migration(database, instance)
