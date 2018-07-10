# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [

    path('pay/<int:payment_id>', views.pay, name='pay'),
    path('update/<int:payment_id>', views.update, name='update'),
    path('result/<int:payment_id>', views.result, name='result'),

]
