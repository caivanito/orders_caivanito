from django.db import models
from django.core import serializers
from api.services import *


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=250, blank=False, verbose_name='Nombre')
    price = models.FloatField(verbose_name='Precio')
    stock = models.PositiveIntegerField(verbose_name='Stock')

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def is_stock(self):
        if self.stock > 1:
            return True
        else:
            return False


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    @property
    def get_total(self):
        order_detail = OrderDetail.objects.get(order_id=self.pk)
        return order_detail.product.price * order_detail.quantity

    @property
    def get_total_usd(self):
        dolar_blue = get_usd('https://www.dolarsi.com/api/api.php?type=valoresprincipales',
                             {'nombre': 'Dolar Blue', 'casa': 'casa'})
        valor_venta = dolar_blue['casa']['venta']
        valor_float = float(valor_venta.replace(',', '.'))
        usd_total = self.get_total / valor_float
        return usd_total

    @property
    def get_orders_details(self):
        orders = serializers.serialize("json", OrderDetail.objects.filter(order_id=self.id))
        return orders


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', verbose_name='Orden')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')

    def save(self, *args, **kwargs):
        product = Product.objects.get(id=self.product.id)
        product.stock = product.stock - self.quantity
        product.save()
        super().save(*args, **kwargs)
