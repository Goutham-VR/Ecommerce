from django.db import models


class Category(models.Model):

    category_name = models.CharField(
        max_length=100,
        unique=True
    )

    category_status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    subcategory_name = models.CharField(
        max_length=100
    )

    subcategory_status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subcategory_name


class Brand(models.Model):

    brand_name = models.CharField(
        max_length=100,
        unique=True
    )

    brand_logo = models.ImageField(
        upload_to='brands/',
        blank=True,
        null=True
    )

    brand_status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.brand_name


class Product(models.Model):

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE
    )

    product_name = models.CharField(
        max_length=200
    )

    product_description = models.TextField()

    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    product_gst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    product_stock = models.IntegerField(
        default=0
    )

    product_status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='products/'
    )

    def __str__(self):
        return self.product.product_name


class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    size = models.CharField(
        max_length=20
    )

    color = models.CharField(
        max_length=30
    )

    stock = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.product.product_name} - {self.size} - {self.color}"