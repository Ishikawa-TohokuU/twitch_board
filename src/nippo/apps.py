from django.apps import AppConfig


class NippoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nippo'
    verbose_name = "日報アプリ"

    def ready(self):
        from .ap_scheduler import start
        start()