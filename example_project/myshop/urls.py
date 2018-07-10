# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import path

from . import views

app_name = "myshop"

urlpatterns = [

    path('', views.home, name='home'),
    path('retry_order/<int:order_id>', views.retry_order, name='retry_order'),

]
