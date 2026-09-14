from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('customer-panel/', views.customer_panel_view, name='customer_panel'),
    path('payment/', views.payment_view, name='payment'),
    path('orders/', views.order_history_view, name='order_history'),
]