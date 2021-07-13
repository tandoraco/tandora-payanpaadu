import logging

from django.conf import settings

from payanpaadu.logger.aws import get_aws_logger


def get_logger(name='application'):
    if settings.DEBUG:
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
        return logger
    elif settings.TESTING:
        logger = logging.getLogger()
        logger.addHandler(logging.NullHandler())
        return logger
    else:
        return get_aws_logger(name)
