from django.apps import AppConfig


class EzoneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ezone"

    def ready(self):
        from . import signals
