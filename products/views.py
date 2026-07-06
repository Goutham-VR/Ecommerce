from django.shortcuts import render
from products.models import Product
# Create your views here.

def productlist(request):
    products = Product.objects.all()
    return render(request, 'products/productlist.html', {'products': products})