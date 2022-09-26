from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartView.as_view(), name='CartView'),
    path('checkout/', views.CheckOutView.as_view(), name='CheckOutView'),
    path('my-orders/', views.MyOrders.as_view(), name='MyOrders'),
    path('all-orders/', views.AllOrdersView.as_view(), name='AllOrdersView'),
]