import logging


def get_logger(name='application'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

