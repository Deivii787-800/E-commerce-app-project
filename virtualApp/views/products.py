from ..models import Products, Category
from ..forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
