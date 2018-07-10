from django.contrib import admin

from myshop.models import Order, OrderPayment


class PaymentInline(admin.StackedInline):
    model = OrderPayment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    pass
