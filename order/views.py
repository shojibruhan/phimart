from django.shortcuts import render
from order import serializers as SZ
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer
from .models import Cart, CartItem, Order, OrderItem
from .services import OrderService
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError  # Import this
from rest_framework.decorators import action
from rest_framework.response import Response


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    # queryset= Cart.objects.all()
    serializer_class= CartSerializer
    permission_classes= [IsAuthenticated]

   
    def perform_create(self, serializer):
        # if Cart.objects.filter(user=self.request.user).exists():
        #     raise serializers.ValidationError("User already has an active cart.")
        serializer.save(user= self.request.user)

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(user= self.request.user)
'''

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the user already has a cart
        if Cart.objects.filter(user=self.request.user).exists():
            raise ValidationError("User already has an active cart.")
        
        # If no existing cart, create a new one
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
'''
class CartItemViewSet(ModelViewSet):
    http_method_names= ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id= self.kwargs['cart_pk'])
    
class OrderViewSet(ModelViewSet):
    http_method_names= ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk= None):
        order= self.get_object()
        OrderService.cancel_order(order= order, user=self.request.user)

        return Response({"status": "Order Canceled"})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk= None):
        order= self.get_object()
        serializer= SZ.UpdateOrderSerializers(order, data= request.data, partial= True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": f"Order Updated to {request.data['status']}"})


    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return SZ.EmptySerializer
        if self.action == 'create':
            return SZ.CreateOrderSerializer
        elif self.action == 'update_status':
            return SZ.UpdateOrderSerializers
        return SZ.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user':self.request.user}
    

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user= self.request.user)