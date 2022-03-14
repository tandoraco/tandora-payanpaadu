import threading

from django.conf import settings

_request_thread = threading.local()


def set_current_database(database_name):
    _request_thread.CURRENT_DATABASE = database_name


def get_current_database():
    if settings.MULTI_TENANT_MODE:
        try:
            return _request_thread.CURRENT_DATABASE
        except AttributeError:
            return None
    else:
        return settings.INSTANCE_DATABASE_NAME


def get_login_database(request):
    if settings.MULTI_TENANT_MODE and request.POST.get('subdomain', ''):
        database = request.POST.get('subdomain', '')
        if isinstance(database, list):
            database = database[0]
    else:
        database = settings.INSTANCE_DATABASE_NAME

    return database


def set_login_database(request):
    database = get_login_database(request)
    set_current_database(database)


def set_database_in_cookie(response):
    response.set_cookie(settings.DB_NAME_COOKIE_KEY, get_current_database())


def get_current_search_index():
    if settings.MULTI_TENANT_MODE:
        try:
            return _request_thread.CURRENT_DATABASE
        except AttributeError:
            return None
    else:
        return settings.INSTANCE_ELASTIC_SEARCH_INDEX
