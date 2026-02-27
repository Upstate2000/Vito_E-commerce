from decimal import Decimal
from typing import Dict, Any

from .cart import Cart


def cart_context(request) -> Dict[str, Any]:
    """
    Context processor que expone el carrito y métricas útiles en las plantillas.

    Devuelve:
      - cart: instancia de Cart (gestor que usa la sesión)
      - cart_count: suma de todas las cantidades (int)
      - cart_total: total del carrito como Decimal

    El resultado se cachea en `request._cart_context` para evitar recalcular
    varias veces durante la misma petición y se adjunta `request.cart` para
    reutilización desde vistas o templates si se desea.
    """
    # Reutilizar si ya fue calculado en esta petición
    cached = getattr(request, "_cart_context", None)
    if cached is not None:
        return cached

    cart = Cart(request)

    # Calcular número total de unidades (suma de cantidades), con tolerancia a datos corruptos
    count = 0
    try:
        for entry in getattr(cart, "cart", {}).values():
            try:
                qty = int(entry.get("quantity", 0))
            except Exception:
                qty = 0
            count += max(0, qty)
    except Exception:
        # Fallback seguro: número de líneas en el dict
        try:
            count = len(cart.cart) if isinstance(cart.cart, dict) else 0
        except Exception:
            count = 0

    # Total como Decimal (Cart.get_total_price ya devuelve Decimal)
    try:
        total = cart.get_total_price()
        if not isinstance(total, Decimal):
            total = Decimal(str(total))
    except Exception:
        total = Decimal("0.00")

    context = {
        "cart": cart,
        "cart_count": count,
        "cart_total": total,
    }

    # Cachear en request para evitar trabajo repetido en la misma petición
    setattr(request, "_cart_context", context)
    # Exponer la instancia del carrito directamente en request para uso interno
    setattr(request, "cart", cart)

    return context