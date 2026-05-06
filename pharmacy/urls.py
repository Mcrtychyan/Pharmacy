from django.contrib import admin
from django.urls import path

from catalog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('categories/', category_list, name='category_list'),
    path('categories/',category_detail, name='category_detail'),

    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),

    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),

    # path('orders/', order_list, name='order_list'),
    # path('orders/', order_detail, name='order_detail'),

    path('reviews/', add_reviews, name='add_reviews'),
]
