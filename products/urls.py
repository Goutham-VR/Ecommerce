from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('productlist/', views.productlist, name='productlist'),
    path('product/<slug:slug>/',views.productdetail,name='productdetail'),
]