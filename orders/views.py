from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from accounts.models import Address

# Create your views here.
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    # cartitems=CartItem.objects.filter(cart=cart)
    cartitems = cart.cartitem_set.all()
    addresses = Address.objects.filter(user=request.user)
    return render(request,'orders/checkout.html',{'cart': cart,'cartitems': cartitems,'addresses': addresses})
