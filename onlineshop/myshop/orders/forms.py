from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'second_name', 'email',
            'address', 'postal_code', 'city'
        ]
