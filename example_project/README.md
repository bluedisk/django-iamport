# Django-Iamport Sample Project

## Setup

#### Install depandancies
```
pip install -r requirements.txt
```

#### Initialize db
```
python manage.py migrate
```

#### Change Iamport Keys in example/settings.py
```
PAYMENT_MERCHANT_ID = '아임포트에서 발급받은 상점 ID'

PAYMENT_REST_KEY = '아임포트에서 발급 받은 REST KEY'
PAYMENT_REST_SECRET = '아임포트에서 발급 받은 REST SECRET'
```

#### Run
```
python manage.py runserver
```

