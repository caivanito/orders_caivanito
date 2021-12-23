from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, renderers
from rest_framework import permissions
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class AddOrderSetView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = AddOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AddOrderSerializer(data=request.data)
        if serializer.is_valid():
            items = request.data['order_details']
            bh = Order.objects.create()
            for item in items:
                od = OrderDetail()
                od.product = Product.objects.get(id=int(item['product']))
                od.quantity = int(item['quantity'])
                od.order = bh
                od.save()
            #     return bh
            return Response({'status': 'order set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for od in instance.order_details.all():
            od.set_stock()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
