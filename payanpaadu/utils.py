import uuid


def get_key():
    return str(uuid.uuid4()).replace('-', '')
