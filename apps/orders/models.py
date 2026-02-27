from django.db import models
from django.conf import settings
from django.urls import reverse

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)      
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # hacerlo opcional evita prompt
    city = models.CharField(max_length=100, blank=True, null=True)         
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id} - {self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('orders:detail', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Usa una referencia en cadena para evitar import directo
    product = models.ForeignKey('catalog.Product', related_name='+', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product}'

    def get_cost(self):
        return self.price * self.quantity