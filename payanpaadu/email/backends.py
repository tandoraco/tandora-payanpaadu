import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

MAIL_GUN_API_ENDPOINT = 'https://api.mailgun.net/v3/mg.tandora.co/messages'


class MailGunBackend(BaseEmailBackend):
    connection = None

    @property
    def auth(self):
        return (
            "api", settings.MAILGUN_API_KEY
        )

    def open(self):
        if not self.connection:
            self.connection = requests.Session()
            self.connection.auth = self.auth

    def send_messages(self, email_messages, files=None):
        self.open()

        for message in email_messages:
            data = {
                "from": f"{settings.TANDORA_APP_NAME} <{message.from_email}>",
                "to": [message.to] if not isinstance(message.to, list) else message.to,
                "subject": message.subject,
                "text": message.body,
            }
            if not files:
                response = self.connection.post(
                    MAIL_GUN_API_ENDPOINT,
                    data=data,
                )
            else:
                response = self.connection.post(
                    MAIL_GUN_API_ENDPOINT,
                    data=data,
                    files=files,
                )

            if settings.DEBUG:
                print(response.ok)
                print(response.content)

        self.close()

    def close(self):
        self.connection.close()
