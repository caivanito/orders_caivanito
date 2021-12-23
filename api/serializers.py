from rest_framework import serializers
from api.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['name', 'price', 'stock']
        fields = '__all__'


class AddOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('product', 'quantity')


class AddOrderSerializer(serializers.ModelSerializer):
    def validate(self, data):
        product_list = []
        for item in data['order_details']:
            product_list.append(item['product'])
        if self.product_duplicate(product_list):
            raise serializers.ValidationError('Existen Productos Duplicados!')
        else:
            product_list = []
            for item in data['order_details']:
                product_list.append(item)
            if self.product_zero(product_list):
                raise serializers.ValidationError('La cantidad debe ser mayor que 0!')
            else:
                if self.product_stock(product_list):
                    return data
                else:
                    raise serializers.ValidationError('No hay Stock!')

    def product_duplicate(self, product_list):
        flag = False
        for item in product_list:
            if product_list.count(item) > 1:
                flag = True
                break
            else:
                flag = False

        if flag:
            return True
        else:
            return False

    def product_stock(self, product_list):
        flag = False
        for item in product_list:
            product_data = item['product']
            quantity = item['quantity']
            product_base = Product.objects.get(id=product_data.id)
            if product_base.stock - quantity > 0:
                flag = True
            else:
                flag = False
                break
        if flag:
            return True
        else:
            return False

    def product_zero(self,product_list):
        flag = False
        for item in product_list:
            quantity = item['quantity']
            if quantity > 0:
                flag = False
            else:
                flag = True
                break
        if flag:
            return True
        else:
            return False

    order_details = AddOrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'date_create', 'order_details', 'get_total', 'get_total_usd')
        read_only = ('id')

