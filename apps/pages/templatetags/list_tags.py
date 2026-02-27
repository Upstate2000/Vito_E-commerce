from django import template

register = template.Library()

@register.filter(name='batch')
def batch(value, n):
    """
    Divide una secuencia en sublistas de tamaño n.
    Uso en plantilla: {{ mylist|batch:4 }}
    Devuelve lista de listas.
    """
    try:
        n = int(n)
        if n <= 0:
            return [value]
    except Exception:
        return [value]

    # Asegurar que value sea iterable y convertir a lista
    try:
        seq = list(value)
    except Exception:
        return [value]

    return [seq[i:i + n] for i in range(0, len(seq), n)]

@register.filter
def chunked(iterable, n):
    """Divide iterable en listas de tamaño n."""
    if not iterable:
        return []
    n = int(n)
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]