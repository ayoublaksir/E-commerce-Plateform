
from django.urls import path
from . import views

urlpatterns = [
    path('', views.detail, name='cart'),
    path('complete/', views.payementComplete, name='complete')

]
