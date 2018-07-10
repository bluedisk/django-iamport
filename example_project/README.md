# Django-Iamport 셈플 프로젝트

## Setup

1. Install depandancies
```
pip install django
```

payment앱 복사
```
cp -rf ../payment .
```

Initialize db
```
python manage.py migrate
```

Change Iamport Keys in example/settings.py
```
PAYMENT_MERCHANT_ID = '아임포트에서 발급받은 상점 ID'

PAYMENT_REST_KEY = '아임포트에서 발급 받은 REST KEY'
PAYMENT_REST_SECRET = '아임포트에서 발급 받은 REST SECRET'
```

Run
```
python manage.py runserver
```

