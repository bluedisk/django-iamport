from django.forms import ModelForm

from myshop.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['_']
