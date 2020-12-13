from datetime import  datetime

from background_task import background
from django.conf import settings


@background(schedule=1)
def ping():
    if settings.DEBUG:
        print(f'Background Job run at {datetime.now()}')
