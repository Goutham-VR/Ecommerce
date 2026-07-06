from django.db import models
from accounts.models import User
from products.models import ProductVariant


class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def grand_total(self):
        return sum(
            item.subtotal
            for item in self.cartitem_set.all()
        )

    def __str__(self):
        return self.user.email


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('cart', 'variant')

    @property
    def subtotal(self):
        return self.variant.variant_price * self.quantity

    def __str__(self):
        return str(self.variant)