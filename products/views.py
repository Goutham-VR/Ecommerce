from django.shortcuts import render
from products.models import Product

def productlist(request):
    products = Product.objects.all()
    return render(request, 'products/productlist.html', {'products': products})

def productdetail(request, slug):
    product = Product.objects.get(
        product_slug=slug
    )

    variants = product.productvariant_set.all()

    return render(
        request,
        'products/productdetail.html',
        {
            'product': product,
            'variants': variants
        }
    )