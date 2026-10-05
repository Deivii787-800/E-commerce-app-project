from ..models import Products
from ..forms import ProductForm
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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