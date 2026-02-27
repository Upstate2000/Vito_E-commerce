# apps/cart/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.apps import apps

from .cart import Cart
from .forms import CartQuantityForm


def _get_product_model():
    """
    Recupera el modelo Product de forma perezosa.
    Ajusta 'apps.catalog.Product' si tu app/model están en otra ruta.
    """
    try:
        return apps.get_model("apps.catalog", "Product")
    except LookupError:
        # Intento alternativo si tu app está registrada como 'catalog'
        try:
            return apps.get_model("catalog", "Product")
        except LookupError:
            raise


def _get_safe_next(request, fallback="cart:detail"):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return next_url
    return resolve_url(fallback)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    Product = _get_product_model()
    product = get_object_or_404(Product, pk=product_id)

    form = CartQuantityForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Cantidad inválida.")
        return redirect(_get_safe_next(request))

    quantity = form.cleaned_data["quantity"]
    override = bool(request.POST.get("update"))

    stock = getattr(product, "stock", None)
    if stock is not None:
        try:
            stock_int = int(stock)
            if stock_int >= 0 and quantity > stock_int:
                messages.warning(request, f"Sólo quedan {stock_int} unidades de «{product.name}». Se ajustó la cantidad.")
                quantity = stock_int
        except Exception:
            pass

    cart = Cart(request)
    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f"«{product.name}» añadido al carro.")
    return redirect(_get_safe_next(request))


@require_POST
def cart_update(request, product_id):
    Product = _get_product_model()
    product = get_object_or_404(Product, pk=product_id)

    form = CartQuantityForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Cantidad inválida.")
        return redirect(_get_safe_next(request))

    quantity = form.cleaned_data["quantity"]
    stock = getattr(product, "stock", None)
    if stock is not None:
        try:
            stock_int = int(stock)
            if stock_int >= 0 and quantity > stock_int:
                messages.warning(request, f"Sólo quedan {stock_int} unidades de «{product.name}». Se ajustó la cantidad.")
                quantity = stock_int
        except Exception:
            pass

    cart = Cart(request)
    cart.update(product=product, quantity=quantity)
    messages.success(request, f"Cantidad de «{product.name}» actualizada.")
    return redirect(_get_safe_next(request))


@require_POST
def cart_remove(request, product_id):
    Product = _get_product_model()
    product = get_object_or_404(Product, pk=product_id)

    cart = Cart(request)
    if product in cart:
        cart.remove(product)
        messages.success(request, f"«{product.name}» eliminado del carro.")
    else:
        messages.info(request, "El producto no estaba en el carro.")
    return redirect(_get_safe_next(request))


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Carro vaciado.")
    return redirect(_get_safe_next(request))