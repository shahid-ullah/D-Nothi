class AutomateProcessDBRouter:
    """
    A router to control all database operations on models in the
    user application.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'automate_process':
            return 'source_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'automate_process':
            return 'source_db'
        return None
