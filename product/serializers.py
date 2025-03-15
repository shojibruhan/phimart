from rest_framework import serializers
from decimal import Decimal
from .models import Category, Product, Review
from django.conf import settings
from django.contrib.auth import get_user_model
'''

class CategorySerializer(serializers.Serializer):
    id= serializers.IntegerField()
    name= serializers.CharField()
    description= serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id= serializers.IntegerField()
    name= serializers.CharField()
    unit_price= serializers.DecimalField(decimal_places=2, max_digits=10, source= 'price')
    # category= serializers.PrimaryKeyRelatedField(
    #     queryset= Category.objects.all()
    # )
    # category= serializers.StringRelatedField()
    # category= CategorySerializer()
    category= serializers.HyperlinkedRelatedField(
        queryset= Category.objects.all(),
        view_name= 'view-specific-category'
    ) 

    price_with_tax= serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)
'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields= ['id', 'name', 'description', 'product_count']

    product_count= serializers.IntegerField(read_only= True)

    # product_count= serializers.SerializerMethodField(method_name='calculate_count')
    
    # def calculate_count(self, category):
    #     count= Product.objects.filter(category= category).count()
    #     return count


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= ['id', 'name', 'description', 'price', 'stock', 'category', 'price_with_tax']

    # category= serializers.PrimaryKeyRelatedField(
    #     queryset= Category.objects.all()
    # ) 
    
    # category= serializers.HyperlinkedRelatedField(
    #     queryset= Category.objects.all(),
    #     view_name= 'view-specific-category'
    # ) 
    
    price_with_tax= serializers.SerializerMethodField(method_name='calculate_tax')

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price can't be negetive")
        return price
    

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)

class SimpleUserSerializer(serializers.ModelSerializer):
    name= serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model= get_user_model()
        fields= ['id', 'name']
    
    def get_current_user_name(self, obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    # user= SimpleUserSerializer()
    user= serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model= Review
        fields= ['id', 'user', 'product', 'ratings', 'comment']
        read_only_fields= ['user', 'product']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    

    def create(self, validated_data):
        product_id= self.context['product_id']
        return Review.objects.create(product_id= product_id, **validated_data)