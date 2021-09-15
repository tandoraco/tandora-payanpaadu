from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from slack_sdk import WebClient
from slack_sdk.oauth import AuthorizeUrlGenerator

from payanpaadu.integrations.slack.constants import SLACK_INSTALLATION_SUCCESS, SLACK_INSTALLATION_FAILED
from payanpaadu.integrations.slack.models import SlackOAuthState
from payanpaadu.integrations.slack.state import ModelStateStore


def oauth_start_helper(request):
    state_store = ModelStateStore()
    state = state_store.issue(request=request)
    authorized_url_generator = AuthorizeUrlGenerator(
        client_id=settings.SLACK_CLIENT_ID,
        scopes=settings.SLACK_OAUTH_SCOPES,
        user_scopes=settings.SLACK_USER_SCOPES,
        redirect_uri=settings.SLACK_REDIRECT_URI
    )
    url = authorized_url_generator.generate(state)
    return f'<a href="{url}">' \
           f'<img alt=""Add to Slack"" height="40" width="139"' \
           'src="https://platform.slack-edge.com/img/add_to_slack.png" ' \
           'srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, ' \
           'https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'


def oauth_callback_helper(request):
    state_store = ModelStateStore()
    code = request.GET['code']
    if state_store.consume(request.GET['state']):
        client = WebClient()
        oauth_response = client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=code
        )
        slack_state = SlackOAuthState.objects.get(uuid=request.GET['state'])
        slack_model = apps.get_model(settings.SLACK_MODEL.split(','))
        slack, _ = slack_model.objects.get_or_create(company=slack_state.company)
        slack.oauth_response = oauth_response.data
        slack.save()
        messages.success(request, message=SLACK_INSTALLATION_SUCCESS)
        return redirect(settings.SLACK_OAUTH_SUCCESS_REDIRECT)
    else:
        messages.error(request, message=SLACK_INSTALLATION_FAILED)
        return redirect(settings.SLACK_OAUTH_FAILURE_REDIRECT)
