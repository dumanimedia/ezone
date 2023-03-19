from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Brand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="products")
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(
        Category, related_name="products", null=True, on_delete=models.SET_NULL
    )
    brand = models.ForeignKey(
        Brand, related_name="products", null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class ProductReview(models.Model):
    CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_msg = models.TextField()
    review_rating = models.CharField(choices=CHOICES, max_length=5)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} --- {self.product.title}"


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    total_cost = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    marchant_id = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return float(int(self.product.price) * int(self.quantity))

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
