from django.urls import path
from . import views


app_name = "virtualApp"

urlpatterns = [
    path("", views.index, name="index"),

    path(
        "products/", 
        views.product, 
        name="products"
        ),

    path(
        "<int:product_id>/", 
        views.product_detail, 
        name="product_detail"
        ),

    path(
        "post-products/", 
        views.post_products, 
        name="post_products"
        ),

    path(
        "create-categorys/", 
        views.create_category, 
        name="create_category"
        ),

    path(
        "signup/", 
        views.signup, 
        name="signup"
        ),

    path(
        "logout/", 
        views.logout_view, 
        name="logout"
        ),

    path(
        "login/", 
        views.login_view, 
        name="login"
        ),

    path(
        "admin-panel/", 
        views.admin_panel, 
        name="admin_panel"
        ),

    path(
        "cart/", 
        views.cart, 
        name="cart"
        ),

    path(
        "cart/add/<int:product_id>/", 
        views.add_to_cart, 
        name="add_to_cart"
        ),

    path(
        "orders/",
        views.order,
        name = "order"
    ),

    path(
        "checkout/",
        views.checkout,
        name = "checkout"
    ),

    path(
        "order-detail/<int:order_id>",
        views.order_detail,
        name = "order_detail"
    ),

    path(
        "cart/delete/<int:item_id>",
        views.remove_from_cart,
        name = "remove_from_cart"
    ),

    path(
        "cart/clear/",
        views.clear_cart,
        name="clear_cart"
    ),

    path(
        "cart/decrease/<int:item_id>",
        views.decrease_quantity,
        name = "decrease_quantity"
    ),

    path(
        "cart/increase/<int:item_id>",
        views.increase_quantity,
        name = "increase_quantity"
    ),

    path(
        "admin-panel/product/<int:product_id>/edit/",
        views.edit_product,
        name = "edit_product"
    ),

    path(
        "admin-panel/product/<int:product_id>/delete/",
        views.delete_product,
        name = "delete_product"
    )

]
