from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from payanpaadu.models import PendingSignup
from payanpaadu.signup.forms import PendingSignupForm
from tandorautils.settings import VERIFY_SUCCESS_PATH

CHECK_EMAIL = 'Please check your email to activate your account.'


@require_GET
@transaction.atomic
def signup(request):
    form = PendingSignupForm(request.GET)
    try:
        form.is_valid()
    except AssertionError:
        pass
    else:
        form.save()

    messages.info(request, message=CHECK_EMAIL)
    return redirect(settings.SIGNUP_SUCCESS_PATH)


@require_GET
@transaction.atomic
def verify_account(request, uuid):
    try:
        signup_obj = PendingSignup.objects.get(hash=uuid, is_verified=False)
    except PendingSignup.DoesNotExist:
        raise Http404
    else:
        request.session['email'] = signup_obj.email
        # we should not do this in a GET, but doing
        # Todo: delete or change this later
        signup_obj.is_verified = True
        signup_obj.save()

    return redirect(VERIFY_SUCCESS_PATH)
