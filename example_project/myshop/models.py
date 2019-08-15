from django.db import models
from django.urls import reverse
from django.utils import timezone

from example import settings
from payment.models import Payment


# 쇼핑몰 내부적으로 사용할 주문 모델
class Order(models.Model):
    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문 목록"

    name = models.CharField('주문명', max_length=100)
    amount = models.PositiveIntegerField('금액')

    email = models.EmailField('이메일', null=True, blank=True)
    buyer = models.CharField('구매자명', max_length=50, null=True, blank=True)
    tel = models.CharField('구매자 연락처', max_length=100)

    addr = models.CharField('구매자 주소', max_length=256, null=True, blank=True)
    subaddr = models.CharField('구매자 주소 나머지', max_length=256, null=True, blank=True)
    postcode = models.CharField('구매자 우편번호', max_length=20, null=True, blank=True)

    PAY_STATUS_CHOCIES = (
        ('ready', '결제 대기'),
        ('confirmed', '결제 완료'),
        ('canceled', '결제 취소'),
    )
    pay_status = models.CharField('결제 상태', max_length=30, default='ready', choices=PAY_STATUS_CHOCIES)

    created_at = models.DateTimeField('생성일자', auto_now_add=True)


# Django-iamport와 연동을 위해 사용할 모델
class OrderPayment(Payment):
    class Meta:
        verbose_name = "제품 결제"
        verbose_name_plural = "제품 결제 목록"

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='payments')

    @staticmethod
    def from_order(order):

        payment = OrderPayment()
        payment.name = '우리상점 : %s' % order.name
        payment.order = order

        payment.amount = order.amount

        payment.buyer_email = order.email
        payment.buyer_name = order.buyer
        payment.buyer_tel = order.tel
        payment.buyer_addr = order.addr + " " + order.subaddr
        payment.buyer_postcode = order.postcode

        # ID 생성하기
        if settings.DEBUG:
            prefix = "myshop_debug"
        else:
            prefix = "myshop"

        now = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M%S')

        payment.uid = "%s_%s_%s" % (prefix, now, order.pk)
        payment.save()

        return payment

    # 결제 완료 후처리 하기(완료 시 호출 됩니다)
    def on_success(self):
        self.order.update(pay_status='confirmed')

    # 취소 발생 시 쇼핑몰에서 동작시킬 처리
    def on_cancel(self):
        self.order.update(pay_status='canceled')  # Payment의 상태는 자동으로 변경됨

    # 결제 재시도 URL
    def get_retry_url(self):
        return reverse('myshop:retry_order', args=[self.order.pk])

    # 결제 후 이동 할 Home URL
    def get_home_url(self):
        return '/'
