from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/<int:order_id>/', views.ViewOrder, name='seller_orders'),
    path('orders/', views.Orders, name='orders_view'),
    path('shipping/<int:order_id>/', views.ShipOrder, name='shipping'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='seller_cancel_order'),
    path('products/', views.Products, name='products'),
    path('add_product/', views.AddProduct.as_view(), name='add_product'),
]