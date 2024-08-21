from django.urls import path

from . import views

urlpatterns = [
    path("products/<slug>/", views.product, name="product_page"),
    path("category/<slug>/", views.category, name="category_page"),
]