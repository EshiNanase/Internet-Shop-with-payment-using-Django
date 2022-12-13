from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иван'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иванов'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'ivan.ivanov@ivan.com'
    }), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Улица Пушкина, дом Колотушкина'
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
