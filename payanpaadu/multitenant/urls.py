from django.urls import path

from payanpaadu.multitenant.views import get_available_sites

urlpatterns = [
    path('available-sites', get_available_sites, name='mas')
]
