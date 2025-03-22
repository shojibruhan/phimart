from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from .models import Product, Category, Review, ProductImage
from .filters import ProductFilters
from .permissions import IsReviewAuthorOrReadOnly
from .paginations import DefaultPagination
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsAdminOrReadOnly, FullDjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema

'''
@api_view(['GET', 'POST'])
def view_product(request):
    if request.method== 'GET':
        products= Product.objects.select_related('category').all()

        
        # serializer= ProductSerializer(products, many= True, context= {'request': request})
        serializer= ProductSerializer(products, many= True)
        return Response(serializer.data)
    if request.method== 'POST':
        # serializer= ProductSerializer(data= request.data, context= {'request': request})
        serializer= ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewProduct(APIView):
    def get(self, request):
        products= Product.objects.select_related('category').all()
        # serializer= ProductSerializer(products, many= True, context= {'request': request})
        serializer= ProductSerializer(products, many= True)

        return Response(serializer.data)
    def post(self, request):
        # serializer= ProductSerializer(data= request.data, context= {'request': request})
        serializer= ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

   
    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    # def get_serializer_class(self):
    #     return ProductSerializer
    

@api_view(['GET', 'PUT', 'DELETE'])
def view_specific_product(request, id):
    if request.method == 'GET':
        # product= Product.objects.get(pk= id)
        product= get_object_or_404(Product, pk=id)
        # pro_dic= {"id": product.id, "name": product.name}
        # serializer= ProductSerializer(product, context= {'request': request})
        serializer= ProductSerializer(product)
        return Response (serializer.data)
    
    if request.method == 'PUT':
        product= get_object_or_404(Product, pk=id)
        serializer= ProductSerializer(product, data= request.data)
        # serializer= ProductSerializer(product, context= {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    if request.method == 'DELETE':
        product= get_object_or_404(Product, pk=id)
        product.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product= get_object_or_404(Product, pk=id)
        serializer= ProductSerializer(product)

        return Response (serializer.data)
    
    def put(self, request, id):
        product= get_object_or_404(Product, pk=id)
        serializer= ProductSerializer(product, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def delete(self, request, id):
        product= get_object_or_404(Product, pk=id)
        product.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view()
def view_category(request):
    categories= Category.objects.annotate(product_count= Count('products')).all()
    serializer= CategorySerializer(categories, many=True)
    return Response(serializer.data)

class ViewCategory(APIView):
    def get(self, request):
        categories= Category.objects.annotate(product_count= Count('products')).all()
        serializer= CategorySerializer(categories, many=True)

        return Response(serializer.data)
    def put(self, request):
        serializer= CategorySerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view()
def view_specific_category(request, pk):
    category= get_object_or_404(Category, pk=pk)
    serializer= CategorySerializer(category)

    return Response(serializer.data)

class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category= get_object_or_404(
            Category.objects.annotate(product_count= Count('products')).all(), 
            pk=pk
        )
        serializer= CategorySerializer(category)
        print("serializer: ", serializer)
        print("serializer.data: ", serializer.data)

        return Response(serializer.data)
    
    def put(self, request, pk):
        category= get_object_or_404(Category.objects.annotate(product_count= Count('products')).all(), pk=pk)
        serializer= CategorySerializer(category, request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)
    
    def delete(self, request, pk):
        category= get_object_or_404(Category.objects.annotate(product_count= Count('products')).all(), pk=pk)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductList(ListCreateAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer
    lookup_field='id'

    # def delete(self, request, id):
    #     product= get_object_or_404(Product, pk=id)
    #     if product.stock > 10:
    #         messeges= "Product with more then 10 stock can't be deleted"
    #         return Response(messeges)
    #     product.delete()
        
        # return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    queryset= Category.objects.annotate(product_count= Count('products')).all()
    serializer_class= CategorySerializer



class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset= Category.objects.annotate(product_count= Count('products')).all()
    serializer_class= CategorySerializer


'''

class ProductViewSet(ModelViewSet):
    """
    API endpoints for managing product and store.
    - Allows authenticated admin to create, update and delete product.
    - Allows User to browse and filter product.
    - Support searching by name, categories and description
    - Support ordering by price and update it
    """
    queryset= Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends= [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields= ['category_id', 'price']
    filterset_class= ProductFilters
    search_fields= ['name', 'description']
    ordering_fields= ['price', 'stock']
    pagination_class= DefaultPagination
    permission_classes= [IsAdminOrReadOnly]
    # permission_classes= [FullDjangoModelPermissions]
    # permission_classes= [DjangoModelPermissionsOrAnonReadOnly]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
    
    @swagger_auto_schema(
            operation_summary="delete operation by admin"
    )
    def destroy(self, request, *args, **kwargs):
        product= self.get_object()
        if product.stock > 10:
            messeges= "Product with more then 10 stock can't be deleted"
            return Response(messeges)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()



class ProductImageViewSet(ModelViewSet):
    serializer_class= ProductImageSerializer
    permission_classes= [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id= self.kwargs.get('product_pk'))






class CategoryViewSet(ModelViewSet):
    queryset= Category.objects.annotate(product_count= Count('products')).all()
    serializer_class= CategorySerializer
    permission_classes= [IsAdminOrReadOnly]

class ReviewViewSet(ModelViewSet):
    # queryset= Review.objects.all()
    serializer_class= ReviewSerializer
    permission_classes= [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id= self.kwargs.get('product_pk'))
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)

    def perform_update(self, serializer):
        serializer.save(user= self.request.user)

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}