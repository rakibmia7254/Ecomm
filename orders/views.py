from django.shortcuts import render, get_object_or_404
from products import models as product_models
from users import models as user_models
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from . import models as order_models
from orders import utiles


def ViewOrder(request, order_id):
    order = get_object_or_404(order_models.Orders, id=order_id)
    if not order.user == request.user:
        return HttpResponseRedirect("/")

    if not order.payment_method == "Cash On Delivery":
        payment_status = utiles.check_payment_status(order.payment_ref.payment_id)
        data = {"order": order, "payment_status": payment_status}
    else:
        data = {"order": order}

    resp = render(request, "orders/order.html", data)
    return resp


def CencelOrder(request, order_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login?next=/orders/")
    order = get_object_or_404(order_models.Orders, id=order_id)
    if not order.user == request.user:
        return HttpResponseRedirect("/")

    order.status = "Cancelled"
    order.save()

    messages.success(request, "Order Cancelled Successfully", "alert-success")
    return HttpResponseRedirect("/")


def add_to_cart(request, slug):
    if "cart" not in request.session or not request.session["cart"]:
        request.session["cart"] = {"cart_count": 0}

    cart = request.session["cart"]
    if not "cart_count" in cart:
        cart["cart_count"] = 0

    if str(slug) in cart:
        cart[str(slug)]["quantity"] += 1
        cart["cart_count"] += 1
    else:
        cart[str(slug)] = {"quantity": 1}
        cart["cart_count"] += 1

    request.session.modified = True
    return HttpResponseRedirect(request.GET.get("next", "/"))


def remove_from_cart(request, slug):
    cart = request.session.get("cart", {})

    if str(slug) in cart:
        request.session["cart"]["cart_count"] -= cart[str(slug)]["quantity"]
        del cart[str(slug)]
        request.session.modified = True

    return HttpResponseRedirect(request.GET.get("next", "/"))


# remove from cart one by one
def remove_one_from_cart(request, slug):
    cart = request.session.get("cart", {})

    if str(slug) in cart:
        cart[str(slug)]["quantity"] -= 1

        if cart[str(slug)]["quantity"] == 0:
            del cart[str(slug)]

        request.session["cart"]["cart_count"] -= 1

        request.session.modified = True

    return HttpResponseRedirect(request.GET.get("next", "/"))


def cart(request):
    if "cart" not in request.session:
        return render(request, "orders/cart.html")
    products = product_models.Products.objects.filter(
        slug__in=request.session.get("cart", {}).keys()
    )
    cart_data = []

    for product in products:
        cart_data.append(
            {
                "name": product.name,
                "price": product.price,
                "slug": product.slug,
                "quantity": request.session["cart"][product.slug]["quantity"],
                "total": product.price
                * request.session["cart"][product.slug]["quantity"],
            }
        )

    subtotal = sum(
        product.price * request.session["cart"][product.slug]["quantity"]
        for product in products
    )
    return render(
        request, "orders/cart.html", {"products": cart_data, "subtotal": subtotal}
    )


def delete_address(request, address_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please Login First", "alert-danger")
        return HttpResponseRedirect("/login")

    try:
        address = user_models.Addresses.objects.get(id=address_id)
    except user_models.Addresses.DoesNotExist:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/profile/")

    if not address.user == request.user:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/profile/")

    address.delete()
    messages.success(request, "Address deleted successfully", "alert-success")
    return HttpResponseRedirect("/profile/")


class CartCheckoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Please Login First", "alert-danger")
            return HttpResponseRedirect("/login?next=/checkout/")

        cart_items = list(request.session.get("cart", {}).keys())
        if "cart_count" in cart_items:
            cart_items.remove("cart_count")

        savedaddress = user_models.Addresses.objects.filter(user=request.user)
        if not savedaddress:
            messages.info(request, "Add Address Before Ordering", "alert-danger")
            return HttpResponseRedirect("/save_address/?next=/checkout/")

        products = product_models.Products.objects.filter(slug__in=cart_items)
        cart_data = []

        for product in products:
            cart_data.append(
                {
                    "name": product.name,
                    "price": product.price,
                    "slug": product.slug,
                    "quantity": request.session["cart"][product.slug]["quantity"],
                    "total": product.price
                    * request.session["cart"][product.slug]["quantity"],
                }
            )

        subtotal = sum(
            product.price * request.session["cart"][product.slug]["quantity"]
            for product in products
        )
        return render(
            request,
            "orders/checkout_cart.html",
            {
                "saved_addresses": savedaddress,
                "products": cart_data,
                "subtotal": subtotal,
            },
        )

    def post(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Please Login First", "alert-danger")
            return HttpResponseRedirect("/login?next=/checkout/")

        payment_method = request.POST.get("payment_method")

        try:
            savedAddresses = user_models.Addresses.objects.get(
                id=request.POST.get("savedAddresses")
            )
        except user_models.Addresses.DoesNotExist:
            messages.info(request, "Please Select Address", "alert-danger")
            return HttpResponseRedirect(f"/checkout/")

        products = product_models.Products.objects.filter(
            slug__in=request.session.get("cart", {}).keys()
        )

        if not products:
            messages.info(request, "Cart is empty", "alert-danger")
            return HttpResponseRedirect(f"/")
        

        inOrder = order_models.CartInOrder.objects.create(
            user=request.user,
        )

        for product in products:
            if product.shop.user == request.user:
                messages.info(request, "You can't order your own product", "alert-danger")
                return HttpResponseRedirect(f"/")

            if product.quantity < request.session["cart"][product.slug]["quantity"]:
                messages.info(request, "Not enough stock", "alert-danger")
                return HttpResponseRedirect(f"/")

            order = order_models.Orders.objects.create(
                user=request.user,
                address=savedAddresses,
                payment_method=payment_method,
                product=product,
                quantity=request.session["cart"][product.slug]["quantity"],
            )
            inOrder.orders_in.add(order)
            order.save()
            product.quantity -= request.session["cart"][product.slug]["quantity"]

        inOrder.place()

        del request.session["cart"]

        if payment_method != "Cash On Delivery":
            return HttpResponseRedirect(f"/paymentCart/{inOrder.id}/")
        messages.success(request, "Order Placed Successfully", "alert-success")

        return HttpResponseRedirect("/")


class CheckoutView(View):
    def get(self, request, slug):
        if not request.user.is_authenticated:
            messages.info(request, "Please Login First", "alert-danger")
            return HttpResponseRedirect("/login?next=/checkout/")

        saved_addresses = user_models.Addresses.objects.filter(user=request.user)

        if not saved_addresses:
            messages.info(request, "Add Address Before Ordering", "alert-danger")
            return HttpResponseRedirect("/save_address/?next=/checkout/")

        product = product_models.Products.objects.get(slug=slug)
        return render(
            request,
            "orders/checkout.html",
            {"product": product, "saved_addresses": saved_addresses},
        )

    def post(self, request, slug):
        if not request.user.is_authenticated:
            messages.info(request, "Please Login First", "alert-danger")
            return HttpResponseRedirect("/login?next=/checkout/")

        try:
            product = product_models.Products.objects.get(slug=slug)
        except product_models.Products.DoesNotExist:
            return HttpResponseRedirect("/")
        
        if product.shop.user == request.user:
            messages.info(request, "You can't order your own product", "alert-danger")
            return HttpResponseRedirect("/")
        

        if product.quantity < request.POST.get("quantity"):
            messages.info(request, "Not enough stock", "alert-danger")
            return HttpResponseRedirect("/")

        payment_method = request.POST.get("payment_method")

        try:
            savedAddresses = user_models.Addresses.objects.get(
                id=request.POST.get("savedAddresses")
            )
        except user_models.Addresses.DoesNotExist:
            messages.info(request, "Please Select Address", "alert-danger")
            return HttpResponseRedirect(f"/checkout/{slug}/")

        order = order_models.Orders.objects.create(
            user=request.user,
            address=savedAddresses,
            payment_method=payment_method,
            total_amount=product.price,
            product=product,
        )
        order.save()

        product.objects.update(in_stock=product.in_stock - order.quantity)


        if payment_method != "Cash On Delivery":
            return HttpResponseRedirect(f"/payment/{order.id}/")

        messages.success(request, "Order Placed Successfully", "alert-success")
        return HttpResponseRedirect("/")


def payment(request, order_id):
    if not request.user.is_authenticated:
        messages.info(request, "Please Login First", "alert-danger")
        return HttpResponseRedirect("/login")

    try:
        order = order_models.Orders.objects.get(id=order_id)
    except order_models.Orders.DoesNotExist:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/")

    if not order.user == request.user:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/")

    if order.payment_method != "Credit Card":
        return HttpResponseRedirect("/")

    payment_session = utiles.create_checkout_session(order)

    if not payment_session:
        return HttpResponseRedirect("/")

    request.session["payment_session"] = payment_session.id
    request.session.modified = True

    payment = order_models.Payment.objects.create(
        order=order, payment_id=payment_session.id
    )

    order.payment_ref = payment
    order.save()

    return HttpResponseRedirect(payment_session.url)



def paymentCart(request, CartOrder_id):

    if not request.user.is_authenticated:
        messages.info(request, "Please Login First", "alert-danger")
        return HttpResponseRedirect("/login")

    try:
        order = order_models.CartInOrder.objects.get(id=CartOrder_id)
    except order_models.CartInOrder.DoesNotExist:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/")

    if not order.user == request.user:
        messages.info(request, "Not found", "alert-danger")
        return HttpResponseRedirect("/")

    if order.orders_in.first().payment_method != "Credit Card":
        return HttpResponseRedirect("/")
    

    payment_session = utiles.create_checkout_session_cart(order)

    if not payment_session:
        return HttpResponseRedirect("/")

    request.session["payment_session"] = payment_session.id
    request.session.modified = True

    for order in order.orders_in.all():
        payment = order_models.Payment.objects.create(
            order=order, payment_id=payment_session.id
        )

        order.payment_ref = payment
        order.save()

    return HttpResponseRedirect(payment_session.url)

def payment_done(request):

    payment_session = request.session.get("payment_session")

    if not payment_session:
        return HttpResponseRedirect("/")

    payModel = order_models.Payment.objects.filter(payment_id=payment_session)

    payModel.update(status=True)

    messages.success(request, "Order Placed Successfully", "alert-success")
    request.session["payment_session"] = None
    return HttpResponseRedirect("/")


def payment_canceled(request):
    payment_session = request.session.get("payment_session")

    if not payment_session:
        return HttpResponseRedirect("/")

    order_models.Payment.objects.filter(payment_id=payment_session).delete()

    messages.info(request, "Payment Canceled", "alert-danger")
    request.session["payment_session"] = None
    return HttpResponseRedirect("/")
