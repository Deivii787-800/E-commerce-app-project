from ..models import Cart, CartItems, Products
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from decimal import Decimal

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(
        user = request.user
    )

    items = cart.items.all()

    subtotal = sum(
        (item.subtotal for item in items),
        Decimal("0")
        )

    return render(request, "cart/cart.html", {
        "cart":cart,
        "items":items,
        "total":subtotal
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id = product_id)

    if not product.is_available:
        messages.error(
            request,
            "El producto no esta disponible"
        )

        return redirect("virtualApp:product_detail", product_id = product.id)

    cart, cart_created = Cart.objects.get_or_create(
        user = request.user
    )

    item, item_created = CartItems.objects.get_or_create(
        cart = cart,
        product = product
    )

    if item.quantity >= product.stock:
        messages.error(
            request,
            "No hay suficiente stock disponible."
        )

        return redirect("virtualApp:product_detail", product_id)

    if not item_created:
        item.quantity += 1
        item.save()

    messages.success(
        request,
        "Producto añadido al carrito."
    )

    return redirect("virtualApp:cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItems,
        id = item_id,
        cart__user = request.user
    )

    item.delete()

    messages.success(
        request,
        f"El producto ha sido eliminado"
    )

    return redirect("virtualApp:cart")

def clear_cart(request):
    cart = get_object_or_404(
        Cart,
        user = request.user
    )

    cart.items.all().delete()

    messages.success(
        request,
        "El carrito ha sido vaciado correctamente"
    )

    return redirect("virtualApp:cart")

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(
        CartItems,
        id = item_id,
        cart__user = request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("virtualApp:cart")

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(
        CartItems,
        id = item_id,
        cart__user = request.user
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()
    else:
        messages.error(
            request,
            "No hay suficientes productos"
        )

    return redirect("virtualApp:cart")
