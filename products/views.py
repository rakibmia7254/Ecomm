from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from . import models as product_models

# @cache_page(60 * 15)
def product(request, slug):
    try:
        product = product_models.Products.objects.get(slug=slug)
    except product_models.Products.DoesNotExist:
        return HttpResponseRedirect("/") # return 404 page
    
    catagories = product_models.Category.objects.all()[:5]

    related_products = product_models.Products.objects.filter(
        category=product.category
    ).exclude(slug=product.slug)[:4]

    return render(
        request,
        "products/product.html",
        {
            "product": product,
            "catagories": catagories,
            "related_products": related_products,
        },
    )



def category(request, slug):
    try:
        category = product_models.Category.objects.get(slug=slug)
    except product_models.Category.DoesNotExist:
        return HttpResponseRedirect("/") # return 404 page
    
    products = product_models.Products.objects.filter(
        category=category
    )

    return render(
        request,
        "products/category.html",
        {
            "category": category,
            "products": products,
        },
    )