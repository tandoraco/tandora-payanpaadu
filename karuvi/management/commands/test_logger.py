from django.core.management import BaseCommand

from payanpaadu.logger import get_logger


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger = get_logger()
        logger.info('logger test ..')
