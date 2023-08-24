"""
Contains routers for database.
"""


class DbRouter:
    """
    A router to control all database operations on models in the all applications.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read any model goes to default.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write to any model go to master.
        """
        return 'master'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the every only appear in the master database.
        """
        return db == 'master'
