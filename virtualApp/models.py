from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Products(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name = "products"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_in_cart"
            )
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.product.name}" 


class ShippingAdress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_adress"
    )

    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("processing", "Procesando"),
        ("shipped", "Enviado"),
        ("delivered", "Entregado"),
        ("cancelled", "Cancelado"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    shipping_adress = models.ForeignKey(
        ShippingAdress,
        on_delete=models.PROTECT
    )

    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"