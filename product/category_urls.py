from django.urls import path
from product import views



urlpatterns = [
    
    # path("", views.view_category, name="categories"),
    # path("", views.ViewCategory.as_view(), name="categories"),
    path("", views.CategoryList.as_view(), name="categories"),
    # path("<int:pk>/", views.view_specific_category, name='view-specific-category'),
    # path("<int:pk>/", views.ViewSpecificCategory.as_view(), name='view-specific-category'),
    path("<int:pk>/", views.CategoryDetails.as_view(), name='view-specific-category'),
]
