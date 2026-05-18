from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('contacts/', views.contacts, name='contacts'),

    # НОВЫЕ URL ДЛЯ ФАРМАЦЕВТА
    path('pharmacy/dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('pharmacy/add-product/', views.add_product, name='add_product'),
    path('pharmacy/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('pharmacy/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
]