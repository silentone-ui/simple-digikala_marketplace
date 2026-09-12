from django.urls import path
from .views import *

app_name = 'accounts' 

urlpatterns = [
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('signup/',signup_view, name='signup'),
    path('profile/',profile_view, name='profile'),
    path('customer-panel/',customer_panel_view, name='customer_panel'),
    path('payment/',payment_view, name='payment'),
]