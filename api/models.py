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
        total = 0
        order_detail = OrderDetail.objects.filter(order_id=self.pk)
        for od in order_detail:
            total = total + (od.product.price * od.quantity)
        return total

    @property
    def get_total_usd(self):
        dolar_blue = get_usd('https://www.dolarsi.com/api/api.php?type=valoresprincipales',
                             {'nombre': 'Dolar Blue', 'casa': 'casa'})
        sale_value = dolar_blue['casa']['venta']
        sale_value_float = float(sale_value.replace(',', '.'))
        usd_total = self.get_total / sale_value_float
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

    def set_stock(self):
        product = Product.objects.get(id=self.product.id)
        product.stock = product.stock + self.quantity
        product.save()
