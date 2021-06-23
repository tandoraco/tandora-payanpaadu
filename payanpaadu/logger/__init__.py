from payanpaadu.logger.aws import get_aws_logger


def get_logger(name='application'):
    return get_aws_logger(name)


