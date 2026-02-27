# apps/catalog/models.py
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_products', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )
    name = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(max_length=220, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    short_description = models.CharField(max_length=255, blank=True, verbose_name='Descripción corta')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Imagen')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    available = models.BooleanField(default=True, verbose_name='Disponible')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    # Campos para footnote / formato
    format = models.CharField("Formato", max_length=100, blank=True, null=True)
    package = models.CharField("Presentación", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Usamos slug para URLs legibles; ajusta si tu URLconf espera pk
        return reverse('catalog:product_detail', args=[self.slug])

    @property
    def footnote(self):
        """
        Devuelve el footnote preferido para mostrar en la plantilla.
        Prioridad: format + package (concatenados) > short_description > ''.
        """
        parts = []
        if self.format:
            parts.append(self.format)
        if self.package:
            parts.append(self.package)
        if parts:
            return " ".join(parts)
        return self.short_description or ""