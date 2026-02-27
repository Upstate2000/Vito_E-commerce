from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('pages/', include('apps.pages.urls', namespace='pages')),

    # Accounts: primero tus vistas personalizadas, luego las vistas de auth de Django
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset, etc.
]

# Servir media en DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)