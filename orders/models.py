from django.db import models
from accounts.models import User, Address
from products.models import ProductVariant

class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.PROTECT)
    order_number = models.CharField(max_length=100,unique=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    supercoin_used = models.IntegerField(default=0)
    final_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=ORDER_STATUS,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)