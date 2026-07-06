from django.urls import path
from adminpanel import views

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('brand/addbrand/', views.addbrand, name='addbrand'),
    path('brand/listbrand/', views.listbrand, name='listbrand'),
    path('brand/deletebrand/<int:brand_id>/', views.deletebrand, name='deletebrand'),
    path('brand/editbrand/<int:brand_id>/', views.editbrand, name='editbrand'),

    path('category/addcategory/', views.addcategory, name='addcategory'),
    path('category/listcategory/', views.listcategory, name='listcategory'),
    path('category/deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),
    path('category/editcategory/<int:category_id>/', views.editcategory, name='editcategory'),

    path('section/addsection/', views.addsection, name='addsection'),
    path('section/listsection/', views.listsection, name='listsection'),
    path('section/deletesection/<int:section_id>/', views.deletesection, name='deletesection'),
    path('section/editsection/<int:section_id>/', views.editsection, name='editsection'),

    path('subcategory/addsubcategory/', views.addsubcategory, name='addsubcategory'),
    path('subcategory/ajaxsection', views.ajaxsection, name='ajaxsection'),
    path('subcategory/listsubcategory/', views.listsubcategory, name='listsubcategory'),
    path('subcategory/deletesubcategory/<int:subcategory_id>/', views.deletesubcategory, name='deletesubcategory'),
    path('subcategory/editsubcategory/<int:subcategory_id>/', views.editsubcategory, name='editsubcategory'),

    path('product/addproduct/', views.addproduct, name='addproduct'),
    path('product/ajaxsubcategory', views.ajaxsubcategory, name='ajaxsubcategory'),
    path('product/listproduct/', views.listproduct, name='listproduct'),
    path('product/editproduct/<int:product_id>/', views.editproduct, name='editproduct'),
    path('product/deleteproduct/<int:product_id>/', views.deleteproduct, name='deleteproduct'),

    path('productimage/listimage/<int:product_id>/', views.listimage, name='listimage'),
    path('productimage/addproductimage/<int:product_id>/', views.addproductimage, name='addproductimage'),
    path('productimage/deleteproductimage/<int:productimage_id>/<int:product_id>/', views.deleteproductimage, name='deleteproductimage'),

    path('productvariant/listvariant/<int:product_id>/', views.listvariant, name='listvariant'),
    path('productvariant/addproductvariant/<int:product_id>/', views.addproductvariant, name='addproductvariant'),
    path('productvariant/deletevarient/<int:productvariant_id>/<int:product_id>/', views.deletevarient, name='deletevarient'),
    path('productvariant/editvarient/<int:productvariant_id>/<int:product_id>/', views.editvarient, name='editvarient'),
    path('productvariant/addvarientstock/<int:productvariant_id>/<int:product_id>/', views.addvarientstock, name='addvarientstock'),
]