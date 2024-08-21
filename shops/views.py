from django.shortcuts import render
from . import models as shop_models
from products import models as product_models
from django.views import View
from django.http import HttpResponseRedirect



def Shop(request, shop_id):
    shop = shop_models.Shops.objects.get(id=shop_id)
    products = product_models.Products.objects.filter(shop=shop)
    return render(request, "shops/shop.html", {"shop": shop, "products": products})


class RegisterShop(View):
    def get(self, request):

        if request.user.is_vendor:
            return HttpResponseRedirect("/seller/dashboard/")
        
        return render(request, "shops/seller_reg.html")
    
    def post(self, request):
        return HttpResponseRedirect("/")