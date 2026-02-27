# apps/catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductSearchForm

PAGE_SIZE = 16  # número de productos por página


def product_list(request, category_slug=None):
    """Lista de productos, opcionalmente filtrados por categoría.
    Orden: alfabético case-insensitive por nombre.
    """
    categories = Category.objects.only('id', 'name', 'slug')
    current_category = None

    qs = Product.objects.filter(available=True).select_related('category').order_by(Lower('name'))

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        qs = qs.filter(category=current_category)

    paginator = Paginator(qs, PAGE_SIZE)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    # Normalizar stock solo en los objetos de la página actual
    for p in products_page:
        try:
            p.stock = int(p.stock) if p.stock is not None else 0
        except Exception:
            p.stock = 0

    context = {
        'categories': categories,
        'current_category': current_category,
        'products': products_page,
    }
    return render(request, 'catalog/product_list.html', context)


def category_products(request, slug):
    """Lista de productos de una categoría concreta (usando slug)."""
    category = get_object_or_404(Category, slug=slug)
    qs = category.products.filter(available=True).select_related('category').order_by(Lower('name'))

    paginator = Paginator(qs, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Normalizar stock solo en los objetos de la página actual
    for p in page_obj:
        try:
            p.stock = int(p.stock) if p.stock is not None else 0
        except Exception:
            p.stock = 0

    return render(request, 'catalog/product_list.html', {
        'products': page_obj,
        'current_category': category,
        'categories': Category.objects.all(),
    })


def product_detail(request, slug):
    """Detalle de un producto por slug."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_search(request):
    """Búsqueda de productos por nombre o descripción (orden alfabético)."""
    q = request.GET.get('q', '').strip()
    if q:
        qs = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        ).filter(available=True).select_related('category').order_by(Lower('name'))
    else:
        qs = Product.objects.none()

    paginator = Paginator(qs, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Normalizar stock solo en los objetos de la página actual
    for p in page_obj:
        try:
            p.stock = int(p.stock) if p.stock is not None else 0
        except Exception:
            p.stock = 0

    return render(request, 'catalog/product_list.html', {
        'products': page_obj,
        'query': q,
        'categories': Category.objects.all(),
    })


def all_categories(request):
    """Listado de todas las categorías."""
    categories = Category.objects.order_by('name')
    return render(request, 'catalog/all_categories.html', {
        'categories': categories
    })


def home(request):
    """Vista de inicio de la app catalog."""
    return render(request, 'catalog/home.html')