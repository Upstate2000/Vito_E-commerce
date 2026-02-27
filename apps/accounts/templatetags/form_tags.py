from django import template
from django.utils.html import format_html
from django.forms.boundfield import BoundField

register = template.Library()

def _parse_attrs(attr_string):
    """
    Convierte 'class:foo;data-x:1' o 'class="foo" id="bar"' en dict.
    Soporta dos formatos simples; aquí usamos el formato 'key:value;key2:value2'
    pero la función add_class usa solo la clave 'class'.
    """
    attrs = {}
    if not attr_string:
        return attrs
    # Soportar formato simple "key:value;key2:value2"
    parts = [p.strip() for p in attr_string.split(';') if p.strip()]
    for part in parts:
        if ':' in part:
            k, v = part.split(':', 1)
            attrs[k.strip()] = v.strip()
    return attrs

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Añade una clase CSS a un campo de formulario.
    Uso: {{ form.field|add_class:"form-control" }}
    Acepta tanto BoundField como widgets ya renderizados.
    """
    if isinstance(field, BoundField):
        existing = field.field.widget.attrs.get('class', '')
        classes = (existing + ' ' + css_class).strip() if existing else css_class
        attrs = field.field.widget.attrs.copy()
        attrs['class'] = classes
        return field.as_widget(attrs=attrs)
    # Si no es BoundField, devolver tal cual
    return field

@register.filter(name='add_attr')
def add_attr(field, attr_string):
    """
    Añade atributos arbitrarios a un campo.
    Uso: {{ form.field|add_attr:"placeholder:Escribe tu nombre;aria-label:Nombre" }}
    Formato: 'key:value;key2:value2'
    """
    if isinstance(field, BoundField):
        attrs = field.field.widget.attrs.copy()
        new_attrs = _parse_attrs(attr_string)
        # fusionar: si 'class' está en new_attrs, concatenar
        if 'class' in new_attrs:
            existing = attrs.get('class', '')
            attrs['class'] = (existing + ' ' + new_attrs['class']).strip() if existing else new_attrs['class']
            new_attrs.pop('class')
        attrs.update(new_attrs)
        return field.as_widget(attrs=attrs)
    return field