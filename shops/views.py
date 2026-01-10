from django.shortcuts import render, redirect
from . import models as shop_models
from products import models as product_models
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from users.models import User
from django.contrib import messages



def Shop(request, shop_id):
    shop = shop_models.Shops.objects.get(id=shop_id)
    products = product_models.Products.objects.filter(shop=shop)
    return render(request, "shops/shop.html", {"shop": shop, "products": products})


class RegisterShop(View):
    def get(self, request):

        if request.user.is_authenticated and request.user.is_vendor:
            return HttpResponseRedirect("/seller/dashboard/")
        
        return render(request, "shops/seller_reg.html")
    
    def post(self, request):
        user = request.user
        
        # 1. Handle Unauthenticated User Registration
        if not user.is_authenticated:
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "shops/seller_reg.html")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return render(request, "shops/seller_reg.html")

            # Extract username from email
            username = email.split('@')[0]
            # Ensure unique username
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)

        # 2. Extract Shop Data
        shop_name = request.POST.get("shop_name")
        shop_description = request.POST.get("shop_description")
        shop_image = request.FILES.get("shop_image")

        # 3. Validation
        if shop_models.Shops.objects.filter(name=shop_name).exists():
            messages.error(request, "Shop name already taken.")
            return render(request, "shops/seller_reg.html")

        # 4. Create Shop and Update User
        user.is_vendor = True
        user.shop_name = shop_name
        user.save()

        shop_models.Shops.objects.create(
            name=shop_name,
            description=shop_description,
            user=user,
            logo=shop_image
        )

        messages.success(request, f"Congratulations! Your shop '{shop_name}' is now active.")
        return redirect("/seller/dashboard/")
