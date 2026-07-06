from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from products.models import ProductVariant


def addtocart(request, variant_id):

    if not request.user.is_authenticated:
        return redirect('accounts:userlogin')

    variant = ProductVariant.objects.get(
        id=request.POST.get('variant_id')
    )

    quantity = int(
        request.POST.get('quantity')
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return redirect('cart:viewcart')

def viewcart(request):

    cart = Cart.objects.get(
        user=request.user
    )

    items = cart.cartitem_set.all()

    return render(
        request,
        'cart/viewcart.html',
        {
            'cart': cart,
            'items': items
        }
    )