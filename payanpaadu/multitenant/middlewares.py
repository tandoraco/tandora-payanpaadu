from django.http import Http404, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from payanpaadu.logger import get_logger
from payanpaadu.multitenant.models import Instance
from payanpaadu.multitenant.thread import set_current_database, get_current_database


def check_and_set_database_to_settings(database):
    from django.conf import settings
    if database == 'default':
        return
    instance = Instance.objects.using('default').get(db_name=database)
    if database not in settings.DATABASES:
        settings.DATABASES[database] = instance.database_config


class MultiTenantMiddleware(MiddlewareMixin):
    logger = get_logger()

    def process_request(self, request):
        from django.conf import settings
        host = request.META.get('HTTP_HOST')
        extra = {
            'request_path': request.path,
            'host': host,
            'multi_tenant_mode': settings.MULTI_TENANT_MODE
        }
        self.logger.info("[multi_tenant_middleware] received request", extra=extra)
        try:
            if settings.MULTI_TENANT_MODE:
                if host not in settings.MAIN_APP_HOSTS:
                    self.logger.info("[multi_tenant_middleware] multitenant mode and host not in main app hosts",
                                     extra=extra)
                    if not host:
                        raise Http404
                    subdomain = host.split('.')[0]
                    self.logger.info("[multi_tenant_middleware] multitenant mode subdomain", extra={
                        'subdomain': subdomain
                    })
                    # subdomain name and database name will be same
                    check_and_set_database_to_settings(subdomain)
                    set_current_database(subdomain)
                elif request.META.get('HTTP_CUSTOM_DOMAIN_SET'):
                    subdomain = request.META['HTTP_CUSTOM_DOMAIN_FORWARDED_TO_SUBDOMAIN']
                    check_and_set_database_to_settings(subdomain)
                    set_current_database(subdomain)
                else:
                    set_current_database(settings.INSTANCE_DATABASE_NAME)
            else:
                database = get_current_database()
                check_and_set_database_to_settings(database)
                set_current_database(database)
        except Instance.DoesNotExist:
            self.logger.info("[multi_tenant_middleware] subdomain not exists, 404 ..", extra={
                'host': host
            })
            raise Http404

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return HttpResponse(status=404)
