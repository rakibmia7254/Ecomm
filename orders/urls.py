from django.urls import path

from . import views


urlpatterns = [
    path("delete_address/<int:address_id>/", views.delete_address, name="delete_address"),
    path("checkout/<slug>/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/", views.CartCheckoutView.as_view(), name="cart_checkout"),
    path("add_to_cart/<slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove_from_cart/<slug>/", views.remove_from_cart, name="remove_from_cart"),
    path("remove_one_from_cart/<slug>/", views.remove_one_from_cart, name="remove_one_from_cart"),

    path("payment/<int:order_id>/", views.payment, name="payment"),
    path("paymentCart/<int:CartOrder_id>/", views.paymentCart, name="paymentCart"),
    path("payment_done/", views.payment_done, name="payment_done"),
    path("payment_cancel/", views.payment_canceled, name="payment_cancel"),

    path("order/<int:order_id>/", views.ViewOrder, name="order"),
    path("cancel_order/<int:order_id>/", views.CencelOrder, name="cancel_order"),

]