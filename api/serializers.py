from rest_framework import serializers
from api.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['name', 'price', 'stock']
        fields = '__all__'


class OrderDetailSerializerSet(serializers.ModelSerializer):
    def validate(self, data):
        product_data = data['product']
        quantity = data['quantity']
        product_base = Product.objects.get(id=product_data.id)
        if product_base.stock - quantity > 0:
            return data
        else:
            raise serializers.ValidationError('No hay Stock!')

    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']
        # read_only = 'order'
        # validators = [self.validate_stock()]


class OrderDetailSerializerList(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'order']
        # read_only = 'order'


class OrderSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date_create', 'get_total', 'get_total_usd', 'get_orders_details']
