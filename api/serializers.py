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


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('order', 'product', 'quantity')


class OrderDetailSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize only invoice head data, not including entries.
    """

    order_details = OrderDetailSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('date_create', 'order_details')


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

    order_details = AddOrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'date_create', 'order_details')
        read_only = ('id')

    # def create(self, validated_data):
    #     items = validated_data.pop('order_details')
    #     bh = Order.objects.create(**validated_data)
    #     for item in items:
    #         OrderDetail.objects.create(order=bh, **item)
    #     return bh
