from django.db import models

# --------------------------
# Category Model
# --------------------------
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_on = models.DateField(blank=True, null=True)
    updated_on = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


# --------------------------
# Units Model
# --------------------------
class Units(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# --------------------------
# Products Model
# --------------------------
class Products(models.Model):
    code = models.CharField(max_length=100, null=False, blank=False, default="PR001")
    barcode_no = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)
    sale_price = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    purchase_price = models.DecimalField(max_digits=13, decimal_places=2, null=True)
    stock_in_hand = models.IntegerField(default=0, null=True)
    order_threshold = models.CharField(max_length=18, null=True)

    unit = models.ForeignKey(Units, related_name='stock_in_hand_unit', null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product_category', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Code: {self.code})"


# --------------------------
# Stock Sale Main
# --------------------------
class StockSaleMain(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    invoice_no = models.BigAutoField(primary_key=True)
    invoice_date = models.DateTimeField(null=True)
    discount = models.IntegerField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice #{self.invoice_no}"


# --------------------------
# Stock Sale Detail
# --------------------------
class StockSaleDetail(models.Model):
    stock_sale_main = models.ForeignKey(StockSaleMain, related_name='sale_detail', null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='product_detail', null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# --------------------------
# Order Model
# --------------------------
class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address1 = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default='0000000000')

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    shipping = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


# --------------------------
# OrderItem Model
# --------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    sale_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


# --------------------------
# Message Model
# --------------------------
class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
