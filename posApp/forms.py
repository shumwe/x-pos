from django import forms
from posApp.models import ProductReturns, TrustedCustomerProfile


class ReturnsForm(forms.ModelForm):
    class Meta:
        model = ProductReturns
        fields = ["product", "return_quantity"]
        widgets = {
            "product": forms.Select(attrs={"style": "width:100%"})
        }

class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = TrustedCustomerProfile
        exclude = ["slug",]