from django.apps import AppConfig

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pages'   # ajusta si tu app está en apps.pages -> 'apps.pages'
    verbose_name = 'Pages'