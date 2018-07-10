# Django-Iamport
Iamport Application for Django

장고용 아임포트 포팅 입니다.
아직 카드 결제만 동작 확인 되었습니다.

# Install
1. git clone
2. payment directory를 프로젝트로 복사
3. setting.py 수정 
```
PAYMENT_MERCHANT_ID = '아임포트에서 발급받은 상점 ID'
PAYMENT_MODEL = 'shop.OrderPayment' # Payment를 상속 받은 주문 모델

# 아임포트 전달 파라메터(그대로 아임포트 모듈에 전달 됩니다)
# IMP.request_pay() 파라메터 : https://github.com/iamport/iamport-manual/blob/master/%EC%9D%B8%EC%A6%9D%EA%B2%B0%EC%A0%9C/README.md

PAYMENT_CONFIG = { 
    'company': '우리 회사', # PG표기 회사명 
    'pg': 'html5_inicis',a  # PG 종류 (아임포트 설정)
    'pay_method': 'card'    # 결제 방법
}
PAYMENT_REST_KEY = '아임포트에서 발급 받은 REST KEY'
PAYMENT_REST_SECRET = '아임포트에서 발급 받은 REST SECRET'
```
4. Payment 모델 상속하기
Payment 모델을 상속 받아서 실제로 사용할 결제 정보 모델을 만들어야 됩니다.
Payment는 다음과 같이 추상 모델로 선언 되어 있습니다.
```
class Payment(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return "%s-%s%s-" % (self.buyer_name, self.amount, self.name)

    name = models.CharField('주문명', max_length=100)

... 중간 생략 ...

    card_id = models.CharField('카드승인번호', max_length=50, null=True, blank=True)

    receipt_url = models.URLField('영수증 URL', null=True, blank=True)

    @staticmethod
    def from_order(order, pay_type):
        raise NotImplementedError()

    def on_success(self):
        raise NotImplementedError()
```

Payment를 상속받은 예제
```
class OrderPayment(Payment):

    class Meta:
        verbose_name = "제품 결제"
        verbose_name_plural = "제품 결제 목록"

    order = models.ForeignKey(Apply, on_delete=models.SET_NULL, null=True, related_name='payments')

    @staticmethod
    def from_order(order):

        payment = OrderPayment()
        payment.name = '우리상점 : %s %s' % order.name
        payment.order = order

        payment.amount = order.roomtype.price

        payment.buyer_email = order.email
        payment.buyer_name = order.name
        payment.buyer_tel = order.cell
        payment.buyer_addr = order.addr + " " + order.subaddr
        payment.buyer_postcode = order.postcode
        payment.save()

        # ID 생성하기
        if settings.DEBUG:
            prefix = "myshop_debug"
        else:
            prefix = "myshop"

        now = timezone.localtime(timezone.now())
        now = now.strftime('%Y%m%d_%H%M%S')

        payment.uid = "%s_%s_%s" % (prefix, now, payment.pk)
        payment.save()

        return payment

    # 결제 완료 후처리 하기(완료 시 호출 됩니다)
    def on_success(self):
        self.order.pay_status = 'confirmed'
        self.order.save()

```

# TODO
~~- REST prepare call~~
~~- card~~
- notification
- vbank
- 후처리 실패시 처리 
- 다중 PG 지원
- 다중 결제 모델 지원 

