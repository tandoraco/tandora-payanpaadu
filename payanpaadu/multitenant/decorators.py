import functools

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from payanpaadu.logger import get_logger


def path_in_main_host_allowed_paths(path):
    return any([path.startswith(_path) for _path in settings.MAIN_HOST_ALLOWED_AUTH_URLS])


def path_in_sub_domain_allowed_paths(path):
    return any([path.startswith(_path) for _path in settings.SUB_DOMAIN_ALLOWED_AUTH_URLS])


def is_allowed_in_multi_tenant_mode(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if not settings.MULTI_TENANT_MODE and not request.path.startswith('/m/'):
            return func(*args, **kwargs)

        host = request.META.get('HTTP_HOST')
        is_request_from_main_host = host in settings.MAIN_APP_HOSTS

        logger = get_logger()
        logger.info("[multi_tenant] is allowed decorator", {
            'host': host,
            'path': request.path,
            'is_request_from_main_host': is_request_from_main_host,
        })

        if is_request_from_main_host and path_in_main_host_allowed_paths(request.path):
            redirect_path = settings.MAIN_HOST_EQUIVALENT_SUBDOMAIN_URLS_DICT.get(request.path)
            if redirect_path:
                return redirect(redirect_path)
            else:
                return func(*args, **kwargs)
        elif not is_request_from_main_host and path_in_sub_domain_allowed_paths(request.path):
            return func(*args, **kwargs)
        else:
            raise Http404

    return wrapper
