from django import forms
from posApp.models import ProductReturns


class ReturnsForm(forms.ModelForm):
    class Meta:
        model = ProductReturns
        fields = ["product", "return_quantity"]
        widgets = {
            "product": forms.Select(attrs={"style": "width:100%"})
        }