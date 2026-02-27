# apps/catalog/templatetags/list_tags.py
from django import template
register = template.Library()

@register.filter
def chunked(iterable, n):
    """Divide iterable en listas de tamaño n."""
    if not iterable:
        return []
    n = int(n)
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]
