from .models import Category

def global_catalog(request):
    categories = Category.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return {
        'categories': categories,
        'cart_count': cart_count,
    }

