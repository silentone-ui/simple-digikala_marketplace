from django.urls import path
from .views import *

app_name = 'marketplace'

urlpatterns = [
    path('',product_list, name='home'),
    path('product/<slug:slug>/',product_detail, name='product_detail'),
    path('cart/',cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/',checkout, name='checkout'),
]