from django.utils.deprecation import MiddlewareMixin

from payanpaadu.custom_domains.models import CustomDomain


class CustomDomainMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            custom_domain = CustomDomain.objects.get(custom_domain=request.META.get('HTTP_HOST', ''), active=True)
            request.META['HTTP_CUSTOM_DOMAIN_SET'] = True
            request.META['HTTP_CUSTOM_DOMAIN_FORWARDED_TO_SUBDOMAIN'] = custom_domain.instance.subdomain
        except CustomDomain.DoesNotExist:
            pass
