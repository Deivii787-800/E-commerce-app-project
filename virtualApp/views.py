from django.shortcuts import render, redirect
from .models import (
    Products,
    Category,
    Cart,
    CartItems,
    Order,
    OrderItem,
    ShippingAdress
)
from django.db import transaction
from django.shortcuts import get_object_or_404
from .forms import ProductForm, ShippingForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, "index.html")


def product(request):
    products = Products.objects.filter(
        is_available = True
    )

    return render(request, "product/products.html", {
        "products":products,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    return render(request, "product/products_details.html", {
        "product":product
    })


@login_required
def post_products(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('virtualApp:products')

    else:
        product_form = ProductForm()


    return render(request, "product/post_products.html", {
        "product_form":product_form
    })

@login_required
def create_category(request):
    if request.method == 'POST':
        category_name = request.POST["category_name"]

        Category.objects.create(
            name = category_name
        )

        return redirect('virtualApp:post_products')

    else:
        return render(request, "product/create_category.html")


@login_required
def admin_panel(request):
    query = request.GET.get('q', '')

    products = Products.objects.filter(user=request.user)

    if query:
        products = products.filter(
            Q(name__icontains = query)|
            Q(description__icontains = query)
        )

    total_products = products.count()


    available_products = products.filter(
        is_available = True,
        stock__gt = 0
    ).count()

    out_of_stock = products.filter(
        stock = 0   
    ).count()

    unavailable_products = products.filter(
        is_available = False
    ).count()

    low_stock = products.filter(
        stock__gt = 0,
        stock__lte = 5
    ).count()

    context = {
        "products":products,
        "query":query,

        "total_products":total_products,
        "available_products":available_products,
        "out_of_stock":out_of_stock,
        "unavailable_products":unavailable_products,
        "low_stock":low_stock,
    }

    return render(request, "admin/admin_panel.html", context)


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(
        Products,
        id = product_id,
        user = request.user
    )

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()

        messages.success(
            request,
            "El producto ha sido modificado correctamente"
        )

        return redirect("virtualApp:admin_panel")

    else:
        form = ProductForm(instance=product)

    return render(request, "product/edit_product.html", {
        "form":form,
        "product":product
    })


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(
        Products,
        id=product_id,
        user=request.user
    )

    if request.method == "POST":

        product.is_available = False
        product.save()

        messages.success(
            request,
            "El producto ha sido desactivado correctamente"
        )

        return redirect("virtualApp:admin_panel")

    return render(
        request,
        "product/delete_product.html",
        {
            "product": product
        }
    )


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



def signup(request):
    if request.method == "GET":
        return render(request, "accounts/signup.html", {
            "form":UserCreationForm()
        })

    form = UserCreationForm(request.POST)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("virtualApp:index")

    return render(request, "accounts/signup.html", {
        "form":form
    })

def login_view(request):
    if request.method == "GET":
        return render(request, "accounts/login.html", {
            "form":AuthenticationForm()
        })

    form = AuthenticationForm(data = request.POST)

    if form.is_valid():
        login(request, form.get_user())
        return redirect("virtualApp:index")

    else:
        return render(request, "accounts/login.html", {
            "form":form
        })

def logout_view(request):
    logout(request)
    return redirect("virtualApp:index")


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


