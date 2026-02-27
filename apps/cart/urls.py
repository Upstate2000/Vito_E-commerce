# apps/cart/urls.py
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    # Vista del detalle del carrito (GET)
    path("", views.cart_detail, name="detail"),

    # Añadir producto al carrito (POST)
    path("add/<int:product_id>/", views.cart_add, name="add"),

    # Actualizar cantidad de un producto (POST)
    path("update/<int:product_id>/", views.cart_update, name="update"),

    # Eliminar producto del carrito (POST)
    path("remove/<int:product_id>/", views.cart_remove, name="remove"),

    # Vaciar el carrito (POST)
    path("clear/", views.cart_clear, name="clear"),
]