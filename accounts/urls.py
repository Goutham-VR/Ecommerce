from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),

    path('address/list/', views.addresslist, name='addresslist'),
    path('address/add/', views.addaddress, name='addaddress'),
    path('address/edit/<int:address_id>/', views.editaddress, name='editaddress'),
    path('address/delete/<int:address_id>/', views.deleteaddress, name='deleteaddress'),
    path('address/default/<int:address_id>/',views.setdefaultaddress,name='setdefaultaddress'),
]