from payanpaadu.multitenant.thread import get_current_database, get_current_search_index


class TandoraDatabaseRouter:

    def db_for_read(self, model, **hints):
        if model.__name__ == 'Instance':
            return 'default'
        return get_current_database()

    def db_for_write(self, model, **hints):
        if model.__name__ == 'Instance':
            return 'default'
        return get_current_database()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


class TandoraSearchRouter:

    def for_read(self, **hints):
        return get_current_search_index()

    def for_write(self, **hints):
        return get_current_search_index()
