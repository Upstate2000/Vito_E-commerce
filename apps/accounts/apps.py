from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'        # ruta del paquete; cámbiala si tu app está en 'accounts'
    verbose_name = 'Cuentas'      # nombre legible en admin
    # label = 'accounts'          # opcional: define un app label distinto si lo necesitas