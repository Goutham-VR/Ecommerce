from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from orders.models import OrderItem
from reviews.models import Review


@login_required
def addreview(request, slug):

    product = Product.objects.get(
        product_slug=slug
    )

    purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status='Delivered',
        variant__product=product
    ).exists()

    if not purchased:
        return redirect(
            'products:productdetail',
            slug
        )

    if Review.objects.filter(
        product=product,
        user=request.user
    ).exists():

        return redirect(
            'products:productdetail',
            slug
        )

    if request.method == "POST":

        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST.get('rating'),
            review=request.POST.get('review')
        )

        return redirect(
            'products:productdetail',
            slug
        )

    return render(
        request,
        'reviews/addreview.html',
        {
            'product': product
        }
    )