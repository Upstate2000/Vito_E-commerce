from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import OrderCreateForm
from .models import Order, OrderItem
from apps.cart.cart import Cart
from django.contrib import messages
from django.db import transaction

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Tu carro está vacío.")
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                # calcular total desde el carrito
                order.total = cart.get_total_price()
                order.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

                # aquí podrías integrar pago; por ahora marcamos como pagado = False
                cart.clear()
                messages.success(request, "Pedido creado correctamente. ID: %s" % order.id)
                return redirect('orders:detail', order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/detail.html', {'order': order})