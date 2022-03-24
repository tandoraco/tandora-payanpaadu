from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payanpaadu.custom_domains.models import CustomDomain
from payanpaadu.multitenant.models import Instance


@csrf_exempt
def get_available_sites(request):
    key = request.META.get('HTTP_KEY')
    if not key == settings.VIRTUAL_HOSTS_POLLING_KEY:
        return HttpResponse('Api key is invalid', status=403)

    subdomains = list(Instance.objects.all().values_list('subdomain', flat=True))
    subdomains = list(
        map(lambda s: settings.MULTI_TENANT_HOST.replace('{subdomain}', s).replace('http://', '').replace('https://',
                                                                                                          ''),
            subdomains))
    custom_domains = list(CustomDomain.objects.all().values_list('custom_domain', flat=True))
    return HttpResponse(','.join(subdomains + custom_domains))
