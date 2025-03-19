from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from product.models import Product
from .services import OrderService



class EmptySerializer(serializers.Serializer):
    pass



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer()
    total_price= serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model= CartItem
        fields= ['id', 'product', 'quantity', 'product', 'total_price']
    
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id= serializers.IntegerField()
    class Meta:
        model= CartItem
        fields= ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id= self.context['cart_id']
        product_id= self.validated_data['product_id']
        quantity= self.validated_data['quantity']

        try:
            cart_item= CartItem.objects.get(cart_id= cart_id, product_id= product_id)
            cart_item.quantity += quantity
            self.instance= cart_item.save()
        except CartItem.DoesNotExist:
            self.instance= CartItem.objects.create(cart_id= cart_id, **self.validated_data)
        
        return self.instance 
    def validate_product_id(self, value):
        if not Product.objects.filter(pk= value).exists():
            raise serializers.ValidationError(f"This Product- id: {value} doesn't exists.")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartItem
        fields= ['quantity']

class CartSerializer(serializers.ModelSerializer):
    items= CartItemSerializer(many= True, read_only= True)
    total_price= serializers.SerializerMethodField()
    class Meta:
        model= Cart
        fields= ['id', 'user', 'items', 'total_price']
        read_only_fields= ['user']
    
    def get_total_price(self, cart: Cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])




class CreateOrderSerializer(serializers.Serializer):
    cart_id= serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk= cart_id).exists():
            raise serializers.ValidationError("No Cart Found")
        
        if not CartItem.objects.filter(cart_id= cart_id).exists():
            raise serializers.ValidationError("Cart is Empty")
        
        return cart_id
    
    def create(self, validated_data):
        user_id= self.context['user_id']
        cart_id= validated_data['cart_id']
        try:
            order= OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        print("\n\ninstance: ", instance)
        print("\n\nOrderSerializer(ninstance)", OrderSerializer(instance))
        print("\n\nOrderSerializer(ninstance).data", OrderSerializer(instance).data)
        return OrderSerializer(instance).data


'''
instance:  Order d4f838e4-1724-4422-b5b7-8ee7e9718e42 by Test - Not Paid


OrderSerializer(ninstance) OrderSerializer(<Order: Order d4f838e4-1724-4422-b5b7-8ee7e9718e42 by Test - Not Paid>):
    id = UUIDField(read_only=True)
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), validators=[<UniqueValidator(queryset=Order.objects.all())>])
    status = ChoiceField(choices=[('Not Paid', 'Not Paid'), ('Ready To Ship', 'Ready To Ship'), ('Shipped', 'Shipped'), ('Deliverd', 'Deliverd'), ('Canceled', 'Canceled')], required=False)
    created_at = DateTimeField(read_only=True)
    items = OrderItemSerializer(many=True):
        id = IntegerField(label='ID', read_only=True)
        product = SimpleProductSerializer():
            id = IntegerField(label='ID', read_only=True)
            name = CharField(max_length=200)
            price = DecimalField(decimal_places=2, max_digits=10)
        quantity = IntegerField()
        price = DecimalField(decimal_places=2, max_digits=10)
    total_price = DecimalField(decimal_places=2, max_digits=10)


OrderSerializer(ninstance).data {
        'id': 'd4f838e4-1724-4422-b5b7-8ee7e9718e42', 
        'user': 2, 'status': 'Not Paid', 
        'created_at': '2025-03-18T21:53:38.682525Z', 
        'items': [{'id': 6, 'product': {'id': 1, 'name': 'Smartphone', 'price': Decimal('213.80')}, 'quantity': 2, 'price': Decimal('213.80')}, {'id': 7, 'product': {'id': 13, 'name': 'Sneakers', 'price': Decimal('86.74')}, 'quantity': 2, 'price': Decimal('86.74')}], 'total_price': Decimal('601.08')}


'''
class UpdateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields= ['status']
    '''
    def update(self, instance, validated_data):
        user= self.context['user']
        new_status= validated_data['status']

        if new_status == Order.CANCELED:
            return OrderService.cancel_order(order= instance, user=user)
        
        if not user.is_staff:
            raise serializers.ValidationError({"details" :"Sorry! You are not allowed to update this order. :)"})
        
        return super().update(instance, validated_data)
    '''

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields= ['id', 'product', 'quantity', 'price']
    product= SimpleProductSerializer()
    # product= serializers.StringRelatedField()

class OrderSerializer(serializers.ModelSerializer):
    items= OrderItemSerializer(many= True)
    class Meta:
        model= Order
        fields= ['id', 'user', 'status', 'created_at', 'items','total_price']