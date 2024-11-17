from django.apps import AppConfig # type: ignore


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

def ready(self):
    import events.signals  # noqa: F401
