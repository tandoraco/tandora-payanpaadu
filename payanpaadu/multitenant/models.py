# Create your models here.
from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.db.models.signals import post_save

from payanpaadu.logger import get_logger
from payanpaadu.multitenant.utils import CreateDatabase


class Instance(models.Model):
    admin_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    company_name = models.CharField(max_length=50, unique=True)
    db_name = models.CharField(max_length=110, unique=True)
    db_user = models.CharField(max_length=100)
    db_password = models.CharField(max_length=50)
    db_host = models.CharField(max_length=20)
    db_port = models.CharField(max_length=4, default=5432)
    subdomain = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'<{self.admin_name}>'

    class Meta:
        db_table = 'master_instance_details'

    @property
    def database_config(self):
        return {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': self.db_name,
            'USER': self.db_user,
            'HOST': self.db_host,
            'PASSWORD': self.db_password,
            'PORT': 5432,
        }


def create_db(sender, instance, created, **kwargs):
    if created and settings.MULTI_TENANT_MODE:
        db_creation = CreateDatabase(instance.db_name, instance.db_user, instance.db_password)
        try:
            db_creation.execute()
            call_command('custom_migrate', f'--database={instance.db_name}')
        except Exception as e:
            logger = get_logger()
            logger.info('[create_db] Exception while creating db', extra={
                'db_name': instance.db_name,
                'exception': str(e)
            })
            db_creation.revert()
            instance.delete()
            raise
    else:
        raise RuntimeError('Only allowed in multitenant mode')


post_save.connect(create_db, sender=Instance)
