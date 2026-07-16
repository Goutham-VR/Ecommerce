from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('checkout/',views.checkout,name="checkout"),
    path('placeorder/',views.placeorder,name="placeorder"),
    path('ordersuccess/<int:order_id>/',views.ordersuccess,name='ordersuccess'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('orderdetail/<int:order_id>/',views.orderdetail,name="orderdetail"),
    path('cancelorder/<int:order_id>/',views.cancelorder,name='cancelorder'),
]