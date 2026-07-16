from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg

from products.models import (Product,Category,Brand)
from reviews.models import Review
from orders.models import OrderItem
from cart.models import Cart
from cart.models import CartItem


def productlist(request):

    search = request.GET.get('search')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')

    products = Product.objects.all()

    # Search
    if search:
        products = products.filter(
            Q(product_name__icontains=search) |
            Q(brand__brand_name__icontains=search)
        )

    # Category Filter
    if category:
        products = products.filter(
            subcategory__section__category_id=category
        )

    # Brand Filter
    if brand:
        products = products.filter(
            brand_id=brand
        )

    # Price Filters
    if min_price:
        products = products.filter(
            productvariant__variant_price__gte=min_price
        )

    if max_price:
        products = products.filter(
            productvariant__variant_price__lte=max_price
        )

    # Sorting
    if sort == "low":
        products = products.order_by(
            'productvariant__variant_price'
        )

    elif sort == "high":
        products = products.order_by(
            '-productvariant__variant_price'
        )

    # Remove duplicate products
    products = products.distinct()

    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(
        request,
        'products/productlist.html',
        {
            'products': products,
            'categories': categories,
            'brands': brands,
            'search': search,
            'category': category,
            'brand': brand,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
        }
    )

def productdetail(request, slug):
    product = Product.objects.get(
        product_slug=slug
    )

    variants = product.productvariant_set.all()

    #review section data
    reviews = Review.objects.filter(product=product).order_by('-id')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_count = reviews.count()
    can_review = False
    if request.user.is_authenticated:
        can_review = OrderItem.objects.filter(order__user=request.user,order__status='Delivered',variant__product=product).exists()
        if Review.objects.filter(product=product,user=request.user).exists():
            can_review = False

    return render(
        request,
        'products/productdetail.html',
        {
            'product': product,
            'variants': variants,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'review_count': review_count,
            'can_review': can_review,
        }
    )