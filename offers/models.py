from django.db import models
from accounts.models import User

class Offer(models.Model):
    OFFER_TYPE = (
        ('PRODUCT', 'Product'),
        ('CATEGORY', 'Category'),
    )
    offer_name = models.CharField(max_length=100)
    offer_type = models.CharField(
        max_length=20,
        choices=OFFER_TYPE,
        default=""
    )
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.offer_name
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50,unique=True)
    discount_percentage = models.DecimalField(max_digits=5,decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=10,decimal_places=2)
    expiry_date = models.DateField()
    max_discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code
    
class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)