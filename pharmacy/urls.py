from django.contrib import admin
from django.urls import path, include

from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('categories/', category_list, name='category_list'),
    path('categories/<slug:slug>/', category_detail, name='category_detail'),

    path('products/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    path('reviews/add/<int:product_id>/', add_reviews, name='add_reviews'),
]
