from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from users import models as user_models
from products import models as product_models
from orders import models as order_models
from shops import models as shop_models
from orders import utiles


def dashboard(request):
    if not request.user.is_authenticated or not request.user.is_vendor:
        messages.error(request, "You are not seller", "alert-danger")
        return HttpResponseRedirect("/login")

    total_order = order_models.Orders.objects.filter(
        product__shop__user=request.user
    ).select_related("product")

    total_products = product_models.Products.objects.filter(
        shop__user=request.user
    ).count()

    total_income = (
        order_models.Orders.objects.filter(product__shop__user=request.user)
        .exclude(status__in=["Cancelled", "Pending"])
        .aggregate(total_income=Sum("total_amount"))
    )

    if total_income["total_income"] is None:
        total_income["total_income"] = 0

    return render(
        request,
        "seller_dashboard/dashboard.html",
        {
            "total_order": total_order.count(),
            "total_products": total_products,
            "orders": total_order,
            "total_income": total_income,
        },
    )


def ViewOrder(request, order_id):
    order = get_object_or_404(order_models.Orders, id=order_id)
    if not order.user == request.user:
        return HttpResponseRedirect("/")

    if not order.payment_method == "Cash On Delivery":
        try:
            payment_status = utiles.check_payment_status(order.payment_ref.payment_id)
        except:
            payment_status = None
        data = {"order": order, "payment_status": payment_status}
    else:
        data = {"order": order}

    resp = render(request, "seller_dashboard/view_order.html", data)
    return resp


def ShipOrder(request, order_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    order = get_object_or_404(order_models.Orders, id=order_id)
    if not order.user == request.user:
        return HttpResponseRedirect("/")

    order.status = "Delivered"
    order.save()

    messages.success(request, "Order Shipped Successfully", "alert-success")
    if request.GET.get("next"):
        return HttpResponseRedirect(request.GET.get("next"))
    return HttpResponseRedirect("/")


def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    order = get_object_or_404(order_models.Orders, id=order_id)
    if not order.user == request.user:
        return HttpResponseRedirect("/")

    order.status = "Cancelled"
    order.save()

    messages.success(request, "Order Cancelled Successfully", "alert-success")
    if request.GET.get("next"):
        return HttpResponseRedirect(request.GET.get("next"))
    return HttpResponseRedirect("/")


class AddProduct(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_vendor:
            messages.error(request, "You are not seller", "alert-danger")
            return HttpResponseRedirect("/login")

        return render(request, "seller_dashboard/add_product.html")

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_vendor:
            messages.error(request, "You are not seller", "alert-danger")
            return HttpResponseRedirect("/login")

        print(request.FILES)

        if not request.FILES.get("image"):
            messages.error(request, "Please add image", "alert-danger")
            return HttpResponseRedirect(request.path_info)

        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category = product_models.Category.objects.get_or_create(
            name=request.POST.get("category"), owner=request.user
        )[0]
        image = request.FILES.get("image")
        shop = shop_models.Shops.objects.get(user=request.user)

        product = product_models.Products.objects.create(
            name=name,
            description=description,
            price=price,
            in_stock=stock,
            category=category,
            image=image,
            shop=shop,
        )
        product.save()
        messages.success(request, "Product Added Successfully", "alert-success")
        if request.GET.get("next"):
            return HttpResponseRedirect(request.GET.get("next"))
        return HttpResponseRedirect("/seller/dashboard/")


def generate_invoice(request, order_id):
    # Get the order details
    Order = order_models.Orders
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{order_id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    # Set the title
    p.setTitle(f"Invoice for Order {order_id}")

    # Start writing the PDF content
    p.drawString(100, 750, "Invoice")
    p.drawString(100, 730, f"Order ID: {order.id}")
    p.drawString(100, 710, f"Customer: {order.address.full_name}")
    p.drawString(100, 690, f"Date: {order.created_at.strftime('%Y-%m-%d')}")

    # List items in the order
    y = 670
    p.drawString(100, y, f"{order.product.name} - ${order.total_amount}")
    y -= 20

    # Total amount
    p.drawString(100, y - 20, f"Total: ${order.total_amount}")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response


def Orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    orders = (
        order_models.Orders.objects.filter(product__shop__user=request.user)
        .select_related("product")
        .order_by("-created_at")
    )

    panding = orders.filter(status="Pending")

    canceled = orders.filter(status="Cancelled")

    completed = orders.filter(status="Delivered")

    return render(
        request,
        "seller_dashboard/orders.html",
        {
            "orders": orders,
            "panding": panding,
            "canceled": canceled,
            "completed": completed,
        },
    )


def Products(request):
    if not request.user.is_authenticated or not request.user.is_vendor:
        messages.error(request, "You are not seller", "alert-danger")
        return HttpResponseRedirect("/login")

    products = product_models.Products.objects.filter(shop__user=request.user)
    return render(request, "seller_dashboard/products.html", {"products": products})
