from django.urls import path
from .views import *

app_name = 'marketplace'

urlpatterns = [
    path('',product_list, name='product_list'),
    path('product/<int:pk>/',product_detail, name='product_detail'),
    path('cart/',cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/',checkout, name='checkout'),
    path('add-balance/',add_balance, name='add_balance'),
    path('orders/',order_history_view, name='order_history'),
]
