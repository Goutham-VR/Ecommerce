from django.urls import path
from wishlist import views

app_name = "wishlist"

urlpatterns = [
    path('addtowishlistfromlist/<int:product_id>/',views.addtowishlistfromlist,name="addtowishlistfromlist"),
    path('add/<int:product_id>/',views.addtowishlist,name='addtowishlist'),
    path('view/',views.viewwishlist,name='viewwishlist'),
    path('remove/<int:item_id>/',views.removewishlistitem,name='removewishlistitem'),
]