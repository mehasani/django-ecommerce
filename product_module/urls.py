from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brands_list'),
    path('product-favorite', views.add_product_to_favorite, name='product_favorite'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail')

]
