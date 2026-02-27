from django.shortcuts import render
from django.templatetags.static import static
from apps.catalog.models import Category


def home_view(request):
    """
    Vista de ejemplo para la home. En producción reemplaza sample_products
    por consultas a tu modelo Product.
    """
    sample_products = [
        {'id':1, 'name':'Patatas Crispy Pops', 'short_description':'Paquete 750 g', 'price':'2,30 €', 'unit':'/ud', 'image_url': static('images/p1.jpg')},
        {'id':2, 'name':'Croquetas Camembert', 'short_description':'Paquete 350 g', 'price':'2,85 €', 'unit':'/ud', 'image_url': static('images/p2.jpg')},
        {'id':3, 'name':'Bizcocho de manzana', 'short_description':'Paquete 600 g', 'price':'4,40 €', 'unit':'/ud', 'image_url': static('images/p3.jpg')},
        {'id':4, 'name':'Snack de lentejas', 'short_description':'Paquete 100 g', 'price':'1,25 €', 'unit':'/ud', 'image_url': static('images/p4.jpg')},
        {'id':5, 'name':'Pizza Kebab', 'short_description':'400 g', 'price':'2,90 €', 'unit':'/ud', 'image_url': static('images/p5.jpg')},
        {'id':6, 'name':'Sepia troceada', 'short_description':'Bandeja 300 g', 'price':'5,95 €', 'unit':'/ud', 'image_url': static('images/p6.jpg')},
    ]

    sections = [
        {'id':'trending', 'title':'Productos del momento', 'view_all_url':'#', 'products': sample_products[:6]},
        {'id':'new', 'title':'Novedades', 'view_all_url':'#', 'products': sample_products[1:5]},
        {'id':'deals', 'title':'Bajadas de precio', 'view_all_url':'#', 'products': sample_products[2:6]},
    ]

    return render(request, 'pages/home.html', {'sections': sections})

from django.shortcuts import render, get_object_or_404
from apps.catalog.models import Category, Product  # ajusta import según tu estructura

def home(request):
    # tu lógica existente...
    categories = Category.objects.all()[:8]

    # Congelados
    try:
        carousel_congelados_category = Category.objects.get(slug='congelados')
        carousel_congelados_products = list(
            carousel_congelados_category.product_set.filter(is_active=True).order_by('-updated')[:12]
        )
    except Category.DoesNotExist:
        carousel_congelados_category = None
        carousel_congelados_products = []

    # Arroz y pasta (slug ejemplo: 'arroz-y-pasta')
    try:
        carousel_arroz_pasta_category = Category.objects.get(slug='arroz-y-pasta')
        carousel_arroz_pasta_products = list(
            carousel_arroz_pasta_category.product_set.filter(is_active=True).order_by('-updated')[:12]
        )
    except Category.DoesNotExist:
        carousel_arroz_pasta_category = None
        carousel_arroz_pasta_products = []

    context = {
        'categories': categories,
        'carousel_congelados_category': carousel_congelados_category,
        'carousel_congelados_products': carousel_congelados_products,
        'carousel_arroz_pasta_category': carousel_arroz_pasta_category,
        'carousel_arroz_pasta_products': carousel_arroz_pasta_products,
        # ... otros contextos
    }
    return render(request, 'home.html', context)

