import logging

import os
import watchtower

from boto3 import Session
from dotenv import load_dotenv
from pythonjsonlogger.jsonlogger import JsonFormatter

LOGGER = None


def get_aws_logging_config():
    load_dotenv()

    boto3_session = Session(
        aws_access_key_id=os.environ.get('AWS_LOGS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_LOGS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_LOGS_REGION_NAME')
    )

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': "%(asctime)s %(levelname)s %(instance_name)s %(name)s "
                          "%(filename)s %(lineno)s %(funcName)s "
                          "%(ip_address)s %(http_method)s %(message)s %(user_agent)",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'watchtower': {
                'level': 'INFO',
                'class': 'watchtower.CloudWatchLogHandler',
                'boto3_session': boto3_session,
                'log_group': os.environ.get('AWS_LOGS_GROUP'),
                'stream_name': os.environ.get('AWS_LOGS_STREAM'),
                'formatter': 'json',
            },
        },
        'loggers': {
            'integration': {
                'level': 'INFO',
                'handlers': ['watchtower'],
                'propagate': False,
            },
            'auth': {
                'level': 'INFO',
                'handlers': ['watchtower'],
                'propagate': False,
            },
            'core': {
                'level': 'INFO',
                'handlers': ['watchtower'],
                'propagate': False,
            },
            'api': {
                'level': 'INFO',
                'handlers': ['watchtower'],
                'propagate': False,
            },
            'application': {
                'level': 'INFO',
                'handlers': ['watchtower'],
                'propagate': False,
            },
        },
    }


def get_aws_logger(name='application'):
    global LOGGER
    if not LOGGER:
        load_dotenv()
        boto3_session = Session(aws_access_key_id=os.environ['AWS_LOGS_ACCESS_KEY_ID'],
                                aws_secret_access_key=os.environ['AWS_LOGS_SECRET_ACCESS_KEY'],
                                region_name=os.environ['AWS_LOGS_REGION_NAME'])

        handler = watchtower.CloudWatchLogHandler(boto3_session=boto3_session)
        handler.setLevel(logging.INFO)
        handler.log_group = os.environ['AWS_LOGS_GROUP']
        handler.stream_name = os.environ['AWS_LOGS_STREAM']
        formatter = JsonFormatter(
            "%(asctime)s %(levelname)s %(instance_name)s %(name)s "
            "%(filename)s %(lineno)s %(funcName)s "
            "%(ip_address)s %(http_method)s %(message)s %(user_agent)")
        formatter.datefmt = "%d/%b/%Y %H:%M:%S"
        handler.formatter = formatter

        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        LOGGER = logger

    return LOGGER
