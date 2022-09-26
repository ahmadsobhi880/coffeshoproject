from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='HomeView'),
    path('about/', views.AboutView.as_view(), name='AboutView'),
    path('FAQ/', views.faq, name='FAQ-Page'),
    path('contact/', views.contact, name='Contact-Page'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

