from django.urls import path
from .views import products, cart, accounts, orders, admin, home


app_name = "virtualApp"

urlpatterns = [
    path("", home.index, name="index"),

    path(
        "products/", 
        products.product, 
        name="products"
        ),

    path(
        "<int:product_id>/", 
        products.product_detail, 
        name="product_detail"
        ),

    path(
        "post-products/", 
        products.post_products, 
        name="post_products"
        ),

    path(
        "create-categorys/", 
        products.create_category, 
        name="create_category"
        ),

    path(
        "signup/", 
        accounts.signup, 
        name="signup"
        ),

    path(
        "logout/", 
        accounts.logout_view, 
        name="logout"
        ),

    path(
        "login/", 
        accounts.login_view, 
        name="login"
        ),

    path(
        "admin-panel/", 
        admin.admin_panel, 
        name="admin_panel"
        ),

    path(
        "cart/", 
        cart.cart, 
        name="cart"
        ),

    path(
        "cart/add/<int:product_id>/", 
        cart.add_to_cart, 
        name="add_to_cart"
        ),

    path(
        "orders/",
        orders.order,
        name = "order"
    ),

    path(
        "checkout/",
        orders.checkout,
        name = "checkout"
    ),

    path(
        "order-detail/<int:order_id>",
        orders.order_detail,
        name = "order_detail"
    ),

    path(
        "cart/delete/<int:item_id>",
        cart.remove_from_cart,
        name = "remove_from_cart"
    ),

    path(
        "cart/clear/",
        cart.clear_cart,
        name="clear_cart"
    ),

    path(
        "cart/decrease/<int:item_id>",
        cart.decrease_quantity,
        name = "decrease_quantity"
    ),

    path(
        "cart/increase/<int:item_id>",
        cart.increase_quantity,
        name = "increase_quantity"
    ),

    path(
        "admin-panel/product/<int:product_id>/edit/",
        admin.edit_product,
        name = "edit_product"
    ),

    path(
        "admin-panel/product/<int:product_id>/delete/",
        admin.delete_product,
        name = "delete_product"
    )

]
