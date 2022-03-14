# Create your models here.
from django.db import models


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

    @property
    def elastic_search_config(self):
        from django.conf import settings
        return {
            'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
            'URL': settings.ELASTIC_SEARCH_URL,
            'INDEX_NAME': self.db_name
        }
