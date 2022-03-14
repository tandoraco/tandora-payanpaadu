import psycopg2
from django.conf import settings

from payanpaadu.logger import get_logger

CREATE_DB_USER = 'create_database_user'
ALTER_USER_PERMISSIONS = 'alter_user_permissions'
CREATE_DB = 'create_database'
GRANT_DB_PRIVILEGE = 'grant_database_privilege_to_user'
ESTABLISH_DB_CONNECTION = 'connect_to_database'
CLOSE_DB_CONNECTION = 'close_database_connection'

DROP_DB = 'drop_database'
DROP_USER = 'drop_user'


class CreateDatabase:
    events = list()

    def __init__(self, database_name, database_user, database_password):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password
        self.connection = None
        self.cursor = None
        self.logger = get_logger()

    def add_events(self):
        self.events.append(ESTABLISH_DB_CONNECTION)
        self.events.append(CREATE_DB_USER)
        self.events.append(ALTER_USER_PERMISSIONS)
        self.events.append(CREATE_DB)
        self.events.append(GRANT_DB_PRIVILEGE)
        self.events.append(CLOSE_DB_CONNECTION)

    def add_reverse_events(self):
        self.events = []
        if not self.connection:
            self.events.append(ESTABLISH_DB_CONNECTION)
        self.events.append(DROP_DB)
        self.events.append(DROP_USER)
        self.events.append(CLOSE_DB_CONNECTION)

    def handle_connect_to_database(self):
        self.connection = psycopg2.connect(database=settings.MASTER_DB_NAME, user=settings.MASTER_DB_USER,
                                           password=settings.MASTER_DB_PASSWORD, host=settings.MASTER_DB_HOST)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def handle_close_database_connection(self):
        self.connection.close()

    def handle_create_database_user(self):
        sql = f"CREATE USER {self.database_user} WITH PASSWORD '{self.database_password}'"
        self.cursor.execute(sql)

    def handle_alter_user_permissions(self):
        sql_statements = [f"ALTER ROLE {self.database_user} SET client_encoding TO 'utf8'",
                          f"ALTER ROLE {self.database_user} SET default_transaction_isolation TO 'read committed'",
                          f"ALTER ROLE {self.database_user} SET timezone TO 'UTC'"]
        for sql in sql_statements:
            self.cursor.execute(sql)

    def handle_create_database(self):
        sql = f"CREATE DATABASE {self.database_name}"
        self.cursor.execute(sql)

    def handle_grant_database_privilege_to_user(self):
        sql = f"GRANT ALL PRIVILEGES ON DATABASE {self.database_name} TO {self.database_user}"
        self.cursor.execute(sql)

    def handle_drop_database(self):
        sql = f'DROP DATABASE {self.database_name}'
        self.cursor.execute(sql)

    def handle_drop_user(self):
        sql = f'DROP USER {self.database_user}'
        self.cursor.execute(sql)

    def handle_events(self):
        for event in self.events:
            func = f'handle_{event}'
            getattr(self, func)()

    def execute(self):
        self.add_events()
        self.handle_events()

    def revert(self):
        self.add_reverse_events()
        self.handle_events()


def set_database_to_settings(company_name, database_host, database_name, database_user, database_password):
    settings.DATABASES[company_name] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database_name,
        'USER': database_user,
        'HOST': database_host,
        'PASSWORD': database_password,
        'PORT': 5432,
    }
