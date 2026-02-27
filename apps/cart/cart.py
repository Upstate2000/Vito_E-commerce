from decimal import Decimal, InvalidOperation
from typing import Dict, Iterator, List, Optional

SESSION_KEY = "cart"


class Cart:
    """
    Gestor de carrito almacenado en sesión.

    - La sesión guarda un dict con claves de producto (id como str).
    - Cada entrada: {'quantity': int, 'price': str}
    - El iterador devuelve items enriquecidos con:
      product, price (Decimal), quantity (int), total_price (Decimal),
      low_stock (bool), is_featured (bool), on_sale (bool)
    - Métodos adicionales: add, update, remove, clear, get_total_price, __len__.
    """

    def __init__(self, request) -> None:
        self.request = request
        self.session = request.session
        self.cart: Dict[str, Dict[str, object]] = self.session.get(SESSION_KEY, {})
        if not isinstance(self.cart, dict):
            self.cart = {}
            self.session[SESSION_KEY] = self.cart

    # -----------------------
    # Mutadores
    # -----------------------
    def add(self, product, quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Añade o actualiza la cantidad de un producto en el carrito.

        - product: instancia del modelo Product
        - quantity: cantidad a añadir o establecer
        - override_quantity: si True reemplaza la cantidad; si False suma
        """
        pid = str(product.id)
        entry = self.cart.get(pid)
        if entry is None:
            # Guardar precio como string para serializar en sesión
            entry = {"quantity": 0, "price": str(product.price)}
            self.cart[pid] = entry

        try:
            qty = int(quantity)
        except Exception:
            qty = 0

        if override_quantity:
            entry["quantity"] = max(0, qty)
        else:
            entry["quantity"] = max(0, int(entry.get("quantity", 0)) + qty)

        self.save()

    def update(self, product, quantity: int) -> None:
        """Establece la cantidad exacta para un producto (equivalente a add(..., override=True))."""
        self.add(product, quantity=quantity, override_quantity=True)

    def remove(self, product) -> None:
        """Elimina un producto del carrito (por id)."""
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self) -> None:
        """Vacía el carrito de la sesión."""
        self.session[SESSION_KEY] = {}
        self.cart = self.session[SESSION_KEY]
        self.save()

    def save(self) -> None:
        """Marca la sesión como modificada para que Django la persista."""
        self.session[SESSION_KEY] = self.cart
        self.session.modified = True

    # -----------------------
    # Lectores / utilidades
    # -----------------------
    def __len__(self) -> int:
        """Número de líneas (entradas) en el carrito."""
        return len(self.cart)

    def __contains__(self, product) -> bool:
        return str(product.id) in self.cart

    def get_item(self, product) -> Optional[Dict[str, object]]:
        """Devuelve la entrada cruda de sesión para un producto o None."""
        return self.cart.get(str(product.id))

    def get_total_price(self) -> Decimal:
        """Devuelve la suma total del carrito como Decimal (seguro frente a datos corruptos)."""
        total = Decimal("0.00")
        for data in self.cart.values():
            try:
                price = Decimal(str(data.get("price", "0")))
                qty = int(data.get("quantity", 0))
                total += price * qty
            except (InvalidOperation, ValueError, TypeError):
                # Ignorar entradas inválidas y continuar
                continue
        return total

    # -----------------------
    # Iteración enriquecida
    # -----------------------
    def __iter__(self) -> Iterator[Dict[str, object]]:
        """
        Iterador que devuelve items enriquecidos:
        {
            'product': Product instance,
            'price': Decimal,
            'quantity': int,
            'total_price': Decimal,
            'low_stock': bool,
            'is_featured': bool,
            'on_sale': bool,
        }
        Mantiene el orden de las claves tal como están en la sesión.
        """
        product_ids: List[str] = list(self.cart.keys())
        if not product_ids:
            return iter([])

        # Importación perezosa para evitar dependencias en import time
        try:
            from catalog.models import Product  # type: ignore
        except Exception:
            return iter([])

        # Recuperar productos existentes
        products = Product.objects.filter(id__in=product_ids)
        prod_map = {str(p.id): p for p in products}

        items: List[Dict[str, object]] = []
        for pid in product_ids:
            data = self.cart.get(pid)
            if not data:
                continue

            product = prod_map.get(pid)
            if not product:
                # Producto eliminado de la BD: opcionalmente podríamos limpiar la sesión aquí
                continue

            # Normalizar cantidad y precio con tolerancia a errores
            try:
                quantity = int(data.get("quantity", 0))
            except Exception:
                quantity = 0

            try:
                price = Decimal(str(data.get("price", str(product.price))))
            except Exception:
                price = Decimal("0.00")

            total_price = price * quantity

            # Flags calculadas desde el producto
            stock_val = getattr(product, "stock", None)
            try:
                stock_int = int(stock_val) if stock_val is not None else None
            except Exception:
                stock_int = None

            item = {
                "product": product,
                "price": price,
                "quantity": quantity,
                "total_price": total_price,
                "low_stock": (stock_int is not None and stock_int <= 5),
                "is_featured": bool(getattr(product, "is_featured", False)),
                "on_sale": bool(getattr(product, "on_sale", False)),
            }
            items.append(item)

        return iter(items)