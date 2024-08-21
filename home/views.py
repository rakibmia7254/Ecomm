from django.shortcuts import render
from django.contrib import messages
from products import models as product_models
from django.http import HttpResponseRedirect
from django.views import View
from . import models as home_models

def home(request):
    if request.session.get("next"): request.session["next"] = None

    if request.session.get("payment_session"): request.session["payment_session"] = None

    products = product_models.Products.objects.all()[:8]
    catagories = product_models.Category.objects.all()[:5]

    return render(
        request, "home/index.html", {"products": products, "catagories": catagories}
    )


class Search(View):
    def get(self, request):
        if request.GET.get("q"):
            q = request.GET.get("q")
            products = product_models.Products.objects.filter(name__icontains=q)[0:10]
            return render(request, "home/search.html", {"products": products, "q": q})
        else:
            return HttpResponseRedirect("/")
        

def subscribe(request):
    email = request.POST.get("email")
    path = request.POST.get("path")
    if email and not home_models.newsletter.objects.filter(email=email).exists():
        home_models.newsletter.objects.create(email=email)
        messages.success(request, "Thank you for subscribing us!", "alert-success")
    else:
        messages.error(request, "Email already exists", "alert-danger")
    return HttpResponseRedirect(path)
