from django.db import models


class Payment(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return "%s-%s%s-" % (self.buyer_name, self.amount, self.name)

    name = models.CharField('주문명', max_length=100)
    amount = models.PositiveIntegerField('금액')
    uid = models.CharField('uid', max_length=100)

    buyer_email = models.EmailField('이메일', null=True, blank=True)
    buyer_name = models.CharField('구매자명', max_length=50, null=True, blank=True)
    buyer_tel = models.CharField('구매자 연락처', max_length=100)
    buyer_addr = models.CharField('구매자 주소', max_length=256, null=True, blank=True)
    buyer_postcode = models.CharField('구매자 우편번호', max_length=20, null=True, blank=True)

    created_at = models.DateTimeField('생성일자', auto_now_add=True)
    updated_at = models.DateTimeField('갱신일자', auto_now=True)

    confirmed_at = models.DateTimeField('결제완료일자', null=True)

    PAY_RESULT_CHOICES = (
        ('ready', '결제 대기'),
        ('success', '결제 성공'),
        ('failed', '결제 실패'),
        ('error', '비정상')
    )
    pay_result = models.CharField('결제 결과', max_length=30, choices=PAY_RESULT_CHOICES, default='ready')

    imp_uid = models.CharField('승인번호', max_length=50, null=True, blank=True)
    imp_result = models.CharField('결제결과', max_length=512, null=True, blank=True)
    pg_tid = models.CharField('PG 승인번호', max_length=50, null=True, blank=True)
    card_id = models.CharField('카드승인번호', max_length=50, null=True, blank=True)

    receipt_url = models.URLField('영수증 URL', null=True, blank=True)

    @staticmethod
    def from_order(order):
        raise NotImplementedError()

    def on_success(self):
        raise NotImplementedError()

    def get_home_url(self):
        raise NotImplementedError()

    def get_retry_url(self):
        raise NotImplementedError()

