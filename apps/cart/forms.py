# apps/cart/forms.py
from django import forms


class CartQuantityForm(forms.Form):
    """
    Valida la cantidad enviada desde los formularios del carrito.
    Mantén mensajes en español para UX coherente.
    """
    quantity = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "Indica la cantidad.",
            "min_value": "La cantidad debe ser al menos 1.",
            "invalid": "Cantidad inválida.",
        },
    )