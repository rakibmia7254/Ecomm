from django.urls import path

from . import views


urlpatterns = [
    path("shop/<int:shop_id>/", views.Shop, name="shop"),
    path("register_shop/", views.RegisterShop.as_view(), name="register_shop"),
]