from django.urls import path
from .views import *

app_name = 'stores'

urlpatterns = [
    path('',store_list_view, name='store_list'),
    path('<int:store_id>/',store_detail_view, name='store_detail'),
    path('seller-panel/',seller_panel_view, name='seller_panel'),
    path('create/',create_store_view, name='create_store'),
    path('add-product/<int:store_id>/',add_product_view, name='add_product'),
    path('delete/<int:store_id>/',delete_store,name='delete_store'),
]

