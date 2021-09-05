from django import forms
from django.apps import apps
from django.conf import settings

from payanpaadu.models import PendingSignup


class PendingSignupForm(forms.ModelForm):
    class Meta:
        model = PendingSignup
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        app_name, model_name = settings.SIGNUP_MODEL.split('.')
        model = apps.get_model(app_name, model_name)
        assert not model.objects.filter(email=email).exists()
        return email
