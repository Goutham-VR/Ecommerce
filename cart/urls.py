from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:variant_id>/',views.addtocart,name='addtocart'),
    path('viewcart/',views.viewcart,name='viewcart'),
]