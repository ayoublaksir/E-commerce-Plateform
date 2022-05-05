from django.urls import path
from . import views


urlpatterns = [
    path('vendor_register/', views.vendor_register.as_view(), name='become_vendor'),
    path('client_register/', views.client_register.as_view(), name='become_client'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),

    path('products/', views.products, name="products"),
    path('products-state/', views.products_state, name="products_state"),
    path('delete_product/<int:pk>', views.product_delete, name='delete_product'),
    path('My_Clients', views.Clients, name='Clients')
]
