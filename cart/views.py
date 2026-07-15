from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from products.models import ProductVariant


def addtocart(request, variant_id):

    if not request.user.is_authenticated:
        return redirect('accounts:userlogin')

    variant = ProductVariant.objects.get(
        id=variant_id
    )

    quantity = int(
        request.POST.get('quantity', 1)
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

        if cart_item.quantity > variant.stock:
            cart_item.quantity = variant.stock

    else:
        cart_item.quantity = min(
            quantity,
            variant.stock
        )

    cart_item.save()

    return redirect(
        'products:productdetail',
        variant.product.product_slug
    )
    # return render(request,'products/productdetail.html',{'msg':"Added to Cart"})

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

def ajaxupdateqnty(request):
    itemid=request.GET.get('itemid')
    qnty=int(request.GET.get('qnty'))
    try:
        data=CartItem.objects.get(id=itemid)
        data.quantity=qnty
        data.save()
    except:
        return redirect('cart:viewcart')