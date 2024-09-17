import os

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if 'TEST' in os.environ:
            return 'default'
        if model._meta.app_label == 'frontend_api':
            return 'frontend_db'
        elif model._meta.app_label == 'admin_api':
            return 'admin_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if 'TEST' in os.environ:
            return 'default'
        if model._meta.app_label == 'frontend_api':
            return 'frontend_db'
        elif model._meta.app_label == 'admin_api':
            return 'admin_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if 'TEST' in os.environ:
            return True
        if app_label == 'frontend_api':
            return db == 'frontend_db'
        elif app_label == 'admin_api':
            return db == 'admin_db'
        return db == 'default'
