from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from decimal import Decimal
from products.models import Brand
from products.models import Category
from products.models import SubCategory
from products.models import Product
from products.models import ProductImage
from products.models import ProductVariant
from products.models import Section
from orders.models import Order
from offers.models import Coupon

#helper Function import
from .utils import generate_coupon_code


# Create your views here.
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

# Brand Views
def addbrand(request):
    if request.method == 'POST':
        # Handle form submission and save the brand
        brand=request.POST.get('brand_name')
        logo=request.FILES.get('brand_logo')

        if Brand.objects.filter(
            brand_name=brand
        ).exists():

            return render(
                request,
                'adminpanel/brand/addbrand.html',
                {
                    'msg': 'Brand already exists'
                }
            )

        Brand.objects.create(brand_name=brand,brand_logo=logo)
        return render(request, 'adminpanel/brand/addbrand.html', {'msg': 'Brand added successfully!'})
    else:
        return render(request, 'adminpanel/brand/addbrand.html')
    
def listbrand(request):
    brands = Brand.objects.all()
    return render(request, 'adminpanel/brand/listbrand.html', {'brands': brands})

def deletebrand(request, brand_id):
    brand = get_object_or_404(Brand,id=brand_id)
    brand.delete()
    return render(request, 'adminpanel/brand/listbrand.html', {'msg': 'Brand deleted successfully!'})

def editbrand(request, brand_id):
    brand = get_object_or_404(Brand,id=brand_id)

    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brand_logo = request.FILES.get('brand_logo')

        if Brand.objects.filter(
            brand_name=brand_name
        ).exclude(id=brand_id).exists():

            return render(
                request,
                'adminpanel/brand/editbrand.html',
                {
                    'msg': 'Brand already exists',
                    'brand': brand
                }
            )

        brand.brand_name = brand_name
        if brand_logo:
            brand.brand_logo = brand_logo
        brand.save()

        return render(
            request,
            'adminpanel/brand/editbrand.html',
            {
                'msg': 'Brand updated successfully!',
                'brand': brand
            }
        )
    else:
        return render(request, 'adminpanel/brand/editbrand.html', {'brand': brand})

# Category Views
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if Category.objects.filter(
            category_name=category_name
        ).exists():

            return render(
                request,
                'adminpanel/category/addcategory.html',
                {
                    'msg': 'Category already exists'
                }
            )

        Category.objects.create(category_name=category_name)
        return render(request, 'adminpanel/category/addcategory.html', {'msg': 'Category added successfully!'})
    else:
        return render(request, 'adminpanel/category/addcategory.html')
    
def listcategory(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/category/listcategory.html', {'categories': categories})

def deletecategory(request, category_id):
    category = get_object_or_404(Category,id=category_id)
    category.delete()
    return render(request, 'adminpanel/category/listcategory.html', {'msg': 'Category deleted successfully!'})

def editcategory(request, category_id):
    category = get_object_or_404(Category,id=category_id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if Category.objects.filter(
            category_name=category_name
        ).exclude(id=category_id).exists():

            return render(
                request,
                'adminpanel/category/editcategory.html',
                {
                    'msg': 'Category already exists',
                    'category': category
                }
            )

        category.category_name = category_name
        category.save()

        return render(
            request,
            'adminpanel/category/editcategory.html',
            {
                'msg': 'Category updated successfully!',
                'category': category
            }
        )
    else:
        return render(request, 'adminpanel/category/editcategory.html', {'category': category})

# Section Views
def addsection(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))

        if Section.objects.filter(
            section_name=section_name,
            category=category_id
        ).exists():

            return render(
                request,
                'adminpanel/section/addsection.html',
                {
                    'msg': 'Section already exists',
                    'categories': categories
                }
            )
        Section.objects.create(section_name=section_name, category=category_id)
        return render(request, 'adminpanel/section/addsection.html', {'msg': 'Section added successfully!'})
    else:
        return render(request, 'adminpanel/section/addsection.html', {'categories': categories})

def listsection(request):
    sections = Section.objects.all()
    return render(request, 'adminpanel/section/listsection.html', {'sections': sections})

def deletesection(request, section_id):
    section = get_object_or_404(Section,id=section_id)
    section.delete()
    return render(request, 'adminpanel/section/listsection.html', {'msg': 'Section deleted successfully!'})

def editsection(request, section_id):
    section = get_object_or_404(Section,id=section_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))

        if Section.objects.filter(
            section_name=section_name,
            category=category_id
        ).exclude(id=section_id).exists():

            return render(
                request,
                'adminpanel/section/editsection.html',
                {
                    'msg': 'Section already exists',
                    'section': section,
                    'categories': categories
                }
            )

        section.section_name = section_name
        section.category = category_id
        section.save()

        return render(
            request,
            'adminpanel/section/editsection.html',
            {
                'msg': 'Section updated successfully!',
                'section': section,
                'categories': categories
            }
        )
    else:
        return render(request, 'adminpanel/section/editsection.html', {'section': section, 'categories': categories})

# SubCategory Views
def addsubcategory(request):
    categories = Category.objects.all()
    sections = Section.objects.all()
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))
        section_id = Section.objects.get(id=request.POST.get('sel_section'))

        if SubCategory.objects.filter(
            subcategory_name=subcategory_name,
            section=section_id
        ).exists():

            return render(
                request,
                'adminpanel/subcategory/addsubcategory.html',
                {
                    'msg': 'Subcategory already exists',
                    'categories': categories,
                    'sections': sections
                }
            )
        SubCategory.objects.create(subcategory_name=subcategory_name,section=section_id)
        return render(request, 'adminpanel/subcategory/addsubcategory.html', {'msg': 'Subcategory added successfully!'})
    else:
        return render(request, 'adminpanel/subcategory/addsubcategory.html', {'categories': categories, 'sections': sections})

def ajaxsection(request):
    category_id = request.GET.get('cid')
    sections = Section.objects.filter(category=category_id)
    return render(request, 'adminpanel/ajaxpages/ajaxsection.html', {'sections': sections})

def listsubcategory(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'adminpanel/subcategory/listsubcategory.html', {'subcategories': subcategories})

def deletesubcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory,id=subcategory_id)
    subcategory.delete()
    return render(request, 'adminpanel/subcategory/listsubcategory.html', {'msg': 'Subcategory deleted successfully!'})

def editsubcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory,id=subcategory_id)
    categories = Category.objects.all()
    sections = Section.objects.filter(category=subcategory.section.category)

    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))
        section_id = Section.objects.get(id=request.POST.get('sel_section'))

        if SubCategory.objects.filter(
            subcategory_name=subcategory_name,
            section=section_id
        ).exclude(id=subcategory_id).exists():

            return render(
                request,
                'adminpanel/subcategory/editsubcategory.html',
                {
                    'msg': 'Subcategory already exists',
                    'subcategory': subcategory,
                    'categories': categories,
                    'sections': sections
                }
            )

        subcategory.subcategory_name = subcategory_name
        subcategory.section = section_id
        subcategory.save()

        return render(
            request,
            'adminpanel/subcategory/editsubcategory.html',
            {
                'msg': 'Subcategory updated successfully!',
                'subcategory': subcategory,
                'categories': categories,
                'sections': sections
            }
        )
    else:
        return render(request, 'adminpanel/subcategory/editsubcategory.html', {'subcategory': subcategory, 'categories': categories, 'sections': sections})

# Product Views
def addproduct(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == 'POST':

        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')

        subcategory = SubCategory.objects.get(
            id=request.POST.get('sel_subcategory')
        )

        brand = Brand.objects.get(
            id=request.POST.get('sel_brand')
        )

        product_gst = request.POST.get('product_gst')
        sku = request.POST.get('sku')

        slug = slugify(product_name)

        if Product.objects.filter(
            product_sku=sku
        ).exists():

            return render(
                request,
                'adminpanel/product/addproduct.html',
                {
                    'categories': categories,
                    'brands': brands,
                    'subcategories': subcategories,
                    'msg': 'SKU already exists'
                }
            )
        
        slug = slugify(product_name)
        count = 1
        temp_slug = slug
        while Product.objects.filter(product_slug=temp_slug).exists():
            count += 1
            temp_slug = f"{slug}-{count}"
            
        slug = temp_slug

        Product.objects.create(
            product_name=product_name,
            product_description=product_description,
            subcategory=subcategory,
            brand=brand,
            product_slug=slug,
            product_sku=sku,
            product_gst=product_gst
        )

        return render(
            request,
            'adminpanel/product/addproduct.html',
            {
                'categories': categories,
                'brands': brands,
                'subcategories': subcategories,
                'msg': 'Product added successfully!'
            }
        )

    return render(
        request,
        'adminpanel/product/addproduct.html',
        {
            'categories': categories,
            'brands': brands,
            'subcategories': subcategories
        }
    )

def ajaxsubcategory(request):
    section_id = request.GET.get('sid')
    subcategories = SubCategory.objects.filter(section=section_id)
    return render(request, 'adminpanel/ajaxpages/ajaxsubcategory.html', {'subcategories': subcategories})

def listproduct(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product/listproduct.html', {'products': products})

def editproduct(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    subcategories = SubCategory.objects.filter(section=product.subcategory.section)
    sections=Section.objects.filter(category=product.subcategory.section.category)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        subcategory_id = SubCategory.objects.get(id=request.POST.get('sel_subcategory'))
        brand_id = Brand.objects.get(id=request.POST.get('sel_brand'))
        product_gst = float(request.POST.get('product_gst'))
        product.product_name = product_name
        product.product_description = product_description
        product.subcategory = subcategory_id
        product.brand = brand_id
        product.product_gst = product_gst
        product.product_sku = request.POST.get('sku')
        product.product_slug = slugify(product_name)
        product.save()

        return render(
            request,
            'adminpanel/product/editproduct.html',
            {
                'msg': 'Product updated successfully!',
                'product': product,
                'categories': categories,
                'brands': brands,
                'subcategories': subcategories,
                'sections':sections
            }
        )
    else:
        return render(request, 'adminpanel/product/editproduct.html', {'product': product, 'categories': categories, 'brands': brands, 'subcategories': subcategories,'sections':sections})
    
def deleteproduct(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    product.delete()
    return render(request, 'adminpanel/product/listproduct.html', {'msg': 'Product deleted successfully!'})

def listimage(request, product_id):
    product_image = ProductImage.objects.filter(product=product_id)
    return render(request, 'adminpanel/productimage/listimage.html', {'product_image': product_image,'product_id': product_id})

def addproductimage(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.method == 'POST':
        product_image = request.FILES.get('product_image')
        product.productimage_set.create(image=product_image,product=product)
        return render(request, 'adminpanel/productimage/addimage.html', {'msg': 'Product image added successfully!', 'product': product,'product_id': product_id})
    else:
        return render(request, 'adminpanel/productimage/addimage.html', {'product': product,'product_id': product_id})
    
def deleteproductimage(request, productimage_id,product_id):
    product_image = get_object_or_404(ProductImage,id=productimage_id)
    product_image.delete()
    return render(request, 'adminpanel/productimage/listimage.html', {'msg': 'Product image deleted successfully!', 'product_id': product_id})

def listvariant(request, product_id):
    product_variant = ProductVariant.objects.filter(product=product_id)
    return render(request, 'adminpanel/variant/listvariant.html', {'product_variant': product_variant,'product_id': product_id})

def addproductvariant(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.method == 'POST':
        size = request.POST.get('size')
        color = request.POST.get('color')
        stock = int(request.POST.get('stock'))
        price = float(request.POST.get('variant_price'))
        product = Product.objects.get(id=product_id)
        ProductVariant.objects.create(
            product=product,
            size=size,
            color=color,
            stock=stock,
            variant_price=price
        )
        return render(request, 'adminpanel/variant/addvariant.html', {'msg': 'Product variant added successfully!', 'product': product,'product_id': product_id})
    else:
        return render(request, 'adminpanel/variant/addvariant.html', {'product': product,'product_id': product_id})
    
def deletevarient(request, productvariant_id,product_id):
    product_variant = get_object_or_404(ProductVariant,id=productvariant_id)
    product_variant.delete()
    return render(request, 'adminpanel/variant/listvariant.html', {'msg': 'Product variant deleted successfully!', 'product_id': product_id})

def addvarientstock(request, productvariant_id,product_id):
    product_variant = get_object_or_404(ProductVariant,id=productvariant_id)
    current_stock = product_variant.stock
    if request.method == 'POST':
        stock = int(request.POST.get('stock'))
        product_variant.stock += stock
        product_variant.save()
        return render(request, 'adminpanel/variant/addvarientstock.html', {'msg': 'Product variant stock updated successfully!', 'product_variant': product_variant,'product_id': product_id,'productvariant_id': productvariant_id,'current_stock': current_stock})
    else:
        return render(request, 'adminpanel/variant/addvarientstock.html', {'product_variant': product_variant,'product_id': product_id,'current_stock': current_stock,'productvariant_id': productvariant_id})
    
def editvarient(request, productvariant_id,product_id):
    product_variant = get_object_or_404(ProductVariant,id=productvariant_id)
    if request.method == 'POST':
        size = request.POST.get('size')
        color = request.POST.get('color')
        stock = int(request.POST.get('stock'))
        price = float(request.POST.get('variant_price'))

        product_variant.size = size
        product_variant.color = color
        product_variant.stock = stock
        product_variant.variant_price = price
        product_variant.save()
        return render(request, 'adminpanel/variant/editvarient.html', {'msg': 'Product variant updated successfully!', 'product_variant': product_variant,'productvariant_id':productvariant_id,'product_id': product_id})
    else:
        return render(request, 'adminpanel/variant/editvarient.html', {'product_variant': product_variant,'product_id': product_id,'productvariant_id':productvariant_id})

#Coupon Section
from datetime import date

def addcoupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('txt_couponcode').strip().upper()
        discount = Decimal(request.POST.get('txt_discount'))
        minimum_amount = Decimal(request.POST.get('txt_minamount'))
        expiry_date = request.POST.get('txt_expirydate')
        max_discount = Decimal(request.POST.get('txt_maxdiscount'))

        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            return render(request,'adminpanel/coupon/addcoupon.html',{'msg': 'Coupon already exists'})

        if discount <= 0 or discount > 100:
            return render(request,'adminpanel/coupon/addcoupon.html',{'msg': 'Discount must be between 1 and 100'})

        if minimum_amount < 0:
            return render(request,'adminpanel/coupon/addcoupon.html',{'msg': 'Minimum amount cannot be negative'})

        if max_discount < 0:
            return render(request,'adminpanel/coupon/addcoupon.html',{'msg': 'Maximum discount cannot be negative'})

        if expiry_date < str(date.today()):
            return render(request,'adminpanel/coupon/addcoupon.html',{'msg': 'Expiry date cannot be in the past'})

        Coupon.objects.create(
            coupon_code=coupon_code,
            discount_percentage=discount,
            minimum_amount=minimum_amount,
            expiry_date=expiry_date,
            max_discount=max_discount
        )
        return render(request,'adminpanel/coupon/addcoupon.html',{'msg':'Coupon Added'})
    else:
        return render(request, 'adminpanel/coupon/addcoupon.html')

def ajaxgeneratecouponcode(request):
    code = generate_coupon_code()
    return HttpResponse(code)

def couponlist(request):
    coupons=Coupon.objects.all()
    return render(request,'adminpanel/coupon/couponlist.html',{'coupons':coupons})

def deletecoupon(request,coupon_id):
    coupon=get_object_or_404(Coupon,id=coupon_id)
    coupon.delete()
    return render(request,'adminpanel/coupon/couponlist.html',{'msg': 'Product variant deleted successfully!'})

def editcoupon(request,coupon_id):
    coupondata=get_object_or_404(Coupon,id=coupon_id)
    if request.method=='POST':
        coupon_code = request.POST.get('txt_couponcode').strip().upper()
        discount = Decimal(request.POST.get('txt_discount'))
        minimum_amount = Decimal(request.POST.get('txt_minamount'))
        expiry_date = request.POST.get('txt_expirydate')
        max_discount = Decimal(request.POST.get('txt_maxdiscount'))

        if Coupon.objects.filter(coupon_code=coupon_code).exclude(id=coupon_id).exists():
            return render(request,'adminpanel/coupon/editcoupon.html',{'editdata': coupondata,'msg': 'Coupon already exists','coupon_id':coupon_id})

        if discount <= 0 or discount > 100:
            return render(request,'adminpanel/coupon/editcoupon.html',{'msg': 'Discount must be between 1 and 100','coupon_id':coupon_id})

        if minimum_amount < 0:
            return render(request,'adminpanel/coupon/editcoupon.html',{'msg': 'Minimum amount cannot be negative','coupon_id':coupon_id})

        if max_discount < 0:
            return render(request,'adminpanel/coupon/editcoupon.html',{'msg': 'Maximum discount cannot be negative','coupon_id':coupon_id})

        if expiry_date < str(date.today()):
            return render(request,'adminpanel/coupon/editcoupon.html',{'msg': 'Expiry date cannot be in the past','coupon_id':coupon_id})
        
        coupondata.coupon_code=coupon_code
        coupondata.discount_percentage=discount
        coupondata.minimum_amount=minimum_amount
        coupondata.expiry_date=expiry_date
        coupondata.max_discount=max_discount
        coupondata.save()
        return render(request,'adminpanel/coupon/editcoupon.html',{'editdata':coupondata,'msg':"Coupon Updated",'coupon_id':coupon_id})
    else:
        return render(request,'adminpanel/coupon/editcoupon.html',{'editdata':coupondata,'coupon_id':coupon_id})

def activate(request,coupon_id):
    coupons=Coupon.objects.all()
    coupondata=get_object_or_404(Coupon,id=coupon_id)
    coupondata.is_active=True
    coupondata.save()
    return render(request,'adminpanel/coupon/couponlist.html',{'coupons':coupons,'msg':"Coupon Activated"})

def deactivate(request,coupon_id):
    coupons=Coupon.objects.all()
    coupondata=get_object_or_404(Coupon,id=coupon_id)
    coupondata.is_active=False
    coupondata.save()
    return render(request,'adminpanel/coupon/couponlist.html',{'coupons':coupons,'msg':"Coupon Deactivated"})

#Order Section
def orderlist(request):
    orders = Order.objects.all().order_by('-id')
    return render(request,'adminpanel/orders/orderlist.html',{'orders': orders})

def orderdetail(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.orderitem_set.all()
    return render(request,'adminpanel/orders/orderdetail.html',{'order': order,'items': items})

def updateorderstatus(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = request.POST.get('status')
    order.save()
    return redirect('adminpanel:orderdetail',order.id)