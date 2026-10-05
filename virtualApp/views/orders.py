from ..models import Cart, OrderItem, Order
from decimal import Decimal
from ..forms import ShippingForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages


@login_required
@transaction.atomic
def checkout(request):
    cart = get_object_or_404(
        Cart, 
        user = request.user
    )

    items = cart.items.select_related("product")

    if not items.exists():
        messages.error(
            request,
            "El producto no existe"
        )

        return redirect("virtualApp:cart")

    if request.method == "POST":
        form = ShippingForm(request.POST)

        for item in items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f"No hay suficiente stock del producto: {item.product.name}"
                )
                return redirect("virtualApp:cart")

            if not item.product.is_available:
                messages.error(
                    request,
                    f"El producto {item.product.name} ya no esta disponible"
                )

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            total = sum(
            (item.subtotal for item in items),
            Decimal("0")
            )   

            order = Order.objects.create(
            user = request.user,
            shipping_adress = address,
            total = total,
            status = "pending"
            )

            for item in items:
                OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )

                item.product.stock -= item.quantity
                item.product.save()

            cart.items.all().delete()
            messages.success(
                request,
                f"Pedido #{order.id}"
            )

            return redirect(
                "virtualApp:order_detail",
                order_id = order.id
                )

    else:
        form = ShippingForm()

    total = sum(
        (item.subtotal for item in items),
        Decimal("0")
    )       

    return render(
        request,
        "orders/checkout.html",
        {
            "form":form,
            "items":items,
            "total":total,
        }
    )

@login_required
def order(request):
    orders = Order.objects.filter(
        user = request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/orders.html", {
            "orders":orders
        }
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id = order_id,
        user = request.user
    )

    return render(
        request, 
        "orders/order_detail.html", {
            'order':order
        }
        )


