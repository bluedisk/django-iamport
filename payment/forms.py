from django import forms

from payment.models import Payment


class PaymentForm(forms.ModelForm):
    class Media:
        js = [
            '//service.iamport.kr/js/iamport.payment-1.1.5.js'
        ]

    class Meta:
        model = Payment
        exclude = ['']

