from django.shortcuts import render
from products.models import Product

def productlist(request):
    products = Product.objects.all()
    return render(request, 'products/productlist.html', {'products': products})