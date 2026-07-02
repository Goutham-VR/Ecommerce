from django.db import models


class Offer(models.Model):

    offer_name = models.CharField(
        max_length=100
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.offer_name
    

class Coupon(models.Model):

    coupon_code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expiry_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.coupon_code