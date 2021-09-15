from django.apps import apps
from django.conf import settings
from django.db import transaction
from slack_sdk.oauth import OAuthStateStore

from payanpaadu.integrations.slack.models import SlackOAuthState
from payanpaadu.logger import get_logger


class ModelStateStore(OAuthStateStore):

    @transaction.atomic
    def issue(self, *args, **kwargs) -> str:
        request = kwargs['request']
        slack_state = SlackOAuthState.objects.create(company=request.user.company)
        return str(slack_state)

    def consume(self, state: str) -> bool:
        try:
            state = SlackOAuthState.objects.get(uuid=state, is_callback_processed=False)
            return state.is_valid()
        except SlackOAuthState.DoesNotExist:
            return False

    @property
    def logger(self):
        return get_logger('integration')
