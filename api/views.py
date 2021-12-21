from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewList(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerList


class OrderDetailViewList(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializerList


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializerSet

    def create(self, request, *args, **kwargs):
        serializer = OrderDetailSerializerSet(data=request.data)
        if serializer.is_valid():

            order = Order()
            order.save()
            serializer.save(order=order)
            return Response({'status': 'order set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = OrderDetailSerializerSet(data=request.data)
        if serializer.is_valid():
            instance = self.get_object()
            instance.order = OrderDetail.objects.get(id=self.get_kwargs()).order
            instance.product = Product.objects.get(id=request.data.get('product'))
            instance.quantity = int(request.data.get('quantity'))
            instance.save()
            return Response({'status': 'order update'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_kwargs(self):
        return self.kwargs.get('pk')
