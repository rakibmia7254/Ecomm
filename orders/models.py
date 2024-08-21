from django.db import models



class Orders(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=100,
        choices=(
            ("Cash On Delivery", "Cash On Delivery"),
            ("Credit Card", "Credit Card"),
        ),
        default="Cash On Delivery",
    )
    total_amount = models.FloatField(null=True, blank=True)
    address = models.ForeignKey("users.Addresses", on_delete=models.CASCADE)
    
    status_choice = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    status = models.CharField(max_length=100, choices=status_choice, default="Pending")
    payment_ref = models.ForeignKey("orders.Payment", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity
        super(Orders, self).save(*args, **kwargs)

class Payment(models.Model):
    order = models.ForeignKey("orders.Orders", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order.id)


class CartInOrder(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    orders_in = models.ManyToManyField("orders.Orders")
    total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.email
    
    def place(self, *args, **kwargs):
        self.total = 0
        for order in self.orders_in.all():

            self.total += order.total_amount
        super(CartInOrder, self).save(*args, **kwargs)


class CartPayment(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    order_cart = models.ForeignKey("orders.CartInOrder", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    status = models.BooleanField(default=False)