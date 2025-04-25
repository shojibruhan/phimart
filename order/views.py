from django.shortcuts import render
from order import serializers as SZ
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer
from .models import Cart, CartItem, Order, OrderItem
from .services import OrderService
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError  # Import this
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ 


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    # queryset= Cart.objects.all()
    serializer_class= CartSerializer
    permission_classes= [IsAuthenticated]

   
    def perform_create(self, serializer):
        # if Cart.objects.filter(user=self.request.user).exists():
        #     raise serializers.ValidationError("User already has an active cart.")
        serializer.save(user= self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none
        return Cart.objects.prefetch_related('items__product').filter(user= self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_cart= Cart.objects.filter(user= request.user).first()

        if existing_cart:
            serializer= self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)

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
        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id= self.kwargs.get('cart_pk'))
    
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
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user':self.request.user}
    

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user= self.request.user)
    
@api_view(['POST'])
def initiate_payment(request):
    user= request.user
    amount= request.data.get("amount")
    order_id= request.data.get("orderId")
    num_items= request.data.get("numItems")
    settings = { 
                'store_id': 'phima680bc9617995d', 
                'store_pass': 'phima680bc9617995d@ssl', 
                'issandbox': True 
                }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"trxn_{order_id}"
    post_body['success_url'] = "http://localhost:5173/dashboard/payment/success/"
    post_body['fail_url'] = "http://localhost:5173/dashboard/payment/success/"
    post_body['cancel_url'] = "http://localhost:5173/dashboard/orders/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-commerce Product"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response

    # Need to redirect user to response['GatewayPageURL']
    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response["GatewayPageURL"]})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)