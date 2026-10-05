from django import forms
from .models import Products, ShippingAdress

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name", "description", "category", "price", "image", "stock", "is_available"]

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            "full_name",
            "address",
            "city",
            "phone"
        ]