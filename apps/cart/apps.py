from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CartConfig(AppConfig):
    """
    Configuración de la aplicación 'cart'.

    - `name` debe coincidir con el path de la app (p. ej. apps.cart).
    - `label` es un identificador corto y único (útil si el nombre del paquete cambia).
    - `verbose_name` está traducido para mostrar en el admin.
    - `ready()` se usa para registrar señales u otras inicializaciones sin
      ejecutar código al importar módulos de modelos.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cart"
    label = "cart"
    verbose_name = _("Carrito")

    def ready(self) -> None:
        """
        Punto de entrada para inicializaciones que deben ejecutarse cuando
        Django carga la aplicación (p. ej. registro de señales).

        Evita errores si el módulo de señales no existe.
        """
        try:
            # Importa aquí el módulo de señales para registrar handlers
            # (crear apps/cart/signals.py si aún no existe).
            from . import signals  # noqa: F401
        except Exception:
            # No fallar si no hay señales o si ocurre un error en importación.
            # En producción podrías registrar el error en el logger si lo deseas.
            pass