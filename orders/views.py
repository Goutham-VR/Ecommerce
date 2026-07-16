from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from accounts.models import Address
from orders.models import Order,OrderItem
import uuid
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    # cartitems=CartItem.objects.filter(cart=cart)
    cartitems = cart.cartitem_set.all()
    addresses = Address.objects.filter(user=request.user)
    return render(request,'orders/checkout.html',{'cart': cart,'cartitems': cartitems,'addresses': addresses})

@login_required
def placeorder(request):
    if request.method != "POST":
        return redirect('orders:checkout')

    cart = Cart.objects.get(user=request.user)
    cartitems = cart.cartitem_set.all()

    if not cartitems.exists():
        return redirect('cart:viewcart')

    address = Address.objects.get(id=request.POST.get('address'),user=request.user)

    for item in cartitems:
        if item.quantity > item.variant.stock:
            return redirect('cart:viewcart')
    
    order = Order.objects.create(
        user=request.user,
        address=address,
        order_number=str(uuid.uuid4())[:8].upper(),
        total_amount=cart.grand_total,
        gst_amount=0,
        discount_amount=0,
        supercoin_used=0,
        final_amount=cart.grand_total
    )

    for item in cartitems:

        if item.quantity > item.variant.stock:
            return redirect('cart:viewcart')

        OrderItem.objects.create(order=order,variant=item.variant,quantity=item.quantity,price=item.variant.variant_price,subtotal=item.subtotal)

        item.variant.stock -= item.quantity
        item.variant.save()

    cartitems.delete()

    return redirect('orders:ordersuccess',order.id)

@login_required
def ordersuccess(request, order_id):
    order = Order.objects.get(id=order_id,user=request.user)
    return render(request,'orders/ordersuccess.html',{'order': order})

@login_required
def orderlist(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request,'orders/orderlist.html',{'orders': orders})

@login_required
def orderdetail(request, order_id):
    order = Order.objects.get(id=order_id,user=request.user)
    items = order.orderitem_set.all()
    return render(request,'orders/orderdetail.html',{'order': order,'items': items})

@login_required
def cancelorder(request, order_id):
    order = Order.objects.get(id=order_id,user=request.user)
    if order.status == "Pending":
        for item in order.orderitem_set.all():
            item.variant.stock += item.quantity
            item.variant.save()

        order.status = "Cancelled"
        order.save()
    return redirect('orders:orderdetail',order.id)