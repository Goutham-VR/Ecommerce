from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
]