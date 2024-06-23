from django.apps import AppConfig


class MapworkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MapWorker'

    def ready(self):
        import MapWorker.signals