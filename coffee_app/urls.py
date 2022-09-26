from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>/', views.CoffeeDetailView.as_view(), name='CoffeeDetailView'),
    path('book_table/', views.BookTableView.as_view(), name='BookTableView'),
    path('bookings/', views.BookingView.as_view(), name='BookingView'),
]