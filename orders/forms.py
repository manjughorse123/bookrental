from django import forms
from .models import OrderAddress

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']