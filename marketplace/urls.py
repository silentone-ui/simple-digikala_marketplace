from django.urls import path
from .views import *

urlpatterns = [
    path('',product_list,name='product_list'),
    path('product/<slug:slug>/',product_detail,name='product_detail')
]
