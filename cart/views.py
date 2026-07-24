from django.shortcuts import render,redirect
from django.http import JsonResponse
from cart.models import Cart, CartItem
from products.models import ProductVariant
from orders.models import Order

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

    try:

        itemid = request.GET.get('itemid')
        qnty = int(request.GET.get('qnty'))

        item = CartItem.objects.get(
            id=itemid,
            cart__user=request.user
        )

        qnty = max(1, qnty)
        qnty = min(qnty, item.variant.stock)

        item.quantity = qnty
        item.save()

        return JsonResponse({
            'success': True,
            'quantity': item.quantity,
            'subtotal': item.subtotal,
            'grand_total': item.cart.grand_total
        })

    except (CartItem.DoesNotExist, ValueError):

        return JsonResponse({
            'success': False
        })
    
def removecartitem(request, citemid):
    CartItem.objects.get(id=citemid,cart__user=request.user).delete()
    return redirect('cart:viewcart')

def ordersuccess(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/ordersuccess.html',
        {
            'order': order
        }
    )