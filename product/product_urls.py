from django.urls import path
from product import views



urlpatterns = [
    # path("", views.view_product, name='products'),
    # path("", views.ViewProduct.as_view(), name='products'),
    path("", views.ProductList.as_view(), name='products'),
    # path("<int:id>/", views.view_specific_product, name='products-list'),
    # path("<int:id>/", views.ViewSpecificProduct.as_view(), name='products-list'),
    path("<int:id>/", views.ProductDetails.as_view(), name='products-list'),
   
]
