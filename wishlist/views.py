from django.shortcuts import render, redirect
from wishlist.models import Wishlist, WishlistItem
from products.models import Product

def addtowishlistfromlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:userlogin')
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist,product=product)
    return redirect('products:productlist')

def addtowishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:userlogin')
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist,product=product)
    return redirect('products:productdetail',product.product_slug)

def viewwishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.wishlistitem_set.all()
    return render(request,'wishlist/viewwishlist.html',{'items': items})

def removewishlistitem(request, item_id):
    WishlistItem.objects.get(id=item_id,wishlist__user=request.user).delete()
    return redirect('wishlist:viewwishlist')