from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager


class CustomUserManager(UserManager):
    def create_vendor(self, username, password, shop_name, **extra_fields):
        extra_fields.setdefault("is_vendor", True)
        if not shop_name:
            raise ValueError("The given shop_name must be set")
        return self.create_user(username, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=100, null=True, blank=True)
    is_vendor = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    profile_image = models.ImageField(
        upload_to="static/users/images", null=True, blank=True
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Addresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


