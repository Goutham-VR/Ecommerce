from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from products.models import Brand
from products.models import Category
from products.models import SubCategory
from products.models import Product
from products.models import ProductImage
from products.models import ProductVariant


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

# SubCategory Views
def addsubcategory(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))

        if SubCategory.objects.filter(
            subcategory_name=subcategory_name,
            category=category_id
        ).exists():

            return render(
                request,
                'adminpanel/subcategory/addsubcategory.html',
                {
                    'msg': 'Subcategory already exists',
                    'categories': categories
                }
            )
        SubCategory.objects.create(subcategory_name=subcategory_name, category=category_id)
        return render(request, 'adminpanel/subcategory/addsubcategory.html', {'msg': 'Subcategory added successfully!'})
    else:
        return render(request, 'adminpanel/subcategory/addsubcategory.html', {'categories': categories})
    
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

    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = Category.objects.get(id=request.POST.get('sel_category'))

        if SubCategory.objects.filter(
            subcategory_name=subcategory_name,
            category=category_id
        ).exclude(id=subcategory_id).exists():

            return render(
                request,
                'adminpanel/subcategory/editsubcategory.html',
                {
                    'msg': 'Subcategory already exists',
                    'subcategory': subcategory,
                    'categories': categories
                }
            )

        subcategory.subcategory_name = subcategory_name
        subcategory.category = category_id
        subcategory.save()

        return render(
            request,
            'adminpanel/subcategory/editsubcategory.html',
            {
                'msg': 'Subcategory updated successfully!',
                'subcategory': subcategory,
                'categories': categories
            }
        )
    else:
        return render(request, 'adminpanel/subcategory/editsubcategory.html', {'subcategory': subcategory, 'categories': categories})

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
    category_id = request.GET.get('cid')
    subcategories = SubCategory.objects.filter(category=category_id)
    return render(request, 'adminpanel/ajaxpages/ajaxsubcategory.html', {'subcategories': subcategories})

def listproduct(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product/listproduct.html', {'products': products})

def editproduct(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    subcategories = SubCategory.objects.filter(category=product.subcategory.category)

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
                'subcategories': subcategories
            }
        )
    else:
        return render(request, 'adminpanel/product/editproduct.html', {'product': product, 'categories': categories, 'brands': brands, 'subcategories': subcategories})
    
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