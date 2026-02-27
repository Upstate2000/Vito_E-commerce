# apps/catalog/templatetags/currency_filters.py
from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(is_safe=True)
def format_cop(value, symbol='$', space=False):
    """
    Formatea un número como moneda colombiana sin decimales y con punto como separador de miles.
    Ejemplo: 1234567.89 -> $ 1.234.568  (redondea al entero más cercano)
    Parámetros:
      - value: Decimal, float, int o string numérico
      - symbol: símbolo de moneda (por defecto '$')
      - space: si True añade un espacio entre símbolo y número (por defecto False)
    """
    if value is None or value == '':
        return ''

    # Convertir a Decimal y redondear al entero más cercano
    try:
        d = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        # Si no es numérico, devolver tal cual (seguro para mostrar)
        return value

    # Redondeo al entero más cercano
    d = d.quantize(Decimal('1'))

    # Formatear con separador de miles (usa coma por defecto), luego reemplazar por punto
    # Ejemplo: format(1234567, ",d") -> '1,234,567' -> '1.234.567'
    try:
        int_value = int(d)
        formatted = format(int_value, ",d").replace(",", ".")
    except Exception:
        formatted = str(d)

    sep = " " if space else ""
    return f"{symbol}{sep}{formatted}"