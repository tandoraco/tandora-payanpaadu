from django.urls import path

from payanpaadu.signup.views import signup, verify_account

urlpatterns = [
    path('signup-free', signup, name='payanpaadu-signup'),
    path('verify-signup/<str:uuid>', verify_account, name='payanpaadu-verify-account')
]
