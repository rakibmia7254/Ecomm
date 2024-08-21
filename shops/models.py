from django.db import models
from users import models as user_models
from products import models as product_models
from django.core.exceptions import ValidationError


class Shops(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    products_owned = models.ManyToManyField(product_models.Products, blank=True)
    logo = models.ImageField(upload_to="static/shops/images", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.user.is_vendor:
            raise ValidationError("Only vendors can own shops.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
