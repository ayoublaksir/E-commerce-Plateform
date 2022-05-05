
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('all_products/', views.all_products, name='all_products'),
    path('my_orders', views.order, name='orders'),
    path('favorites/', views.favorites, name='favorite')
]
