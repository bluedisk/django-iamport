import requests
from django.conf import settings


class IamportRest:
    api_base = 'https://api.iamport.kr/'
    api_auth = '/users/getToken'
    api_prepare = '/payments/prepare'
    api_result = '/payments/'
    api_cancel = '/payments/cancel'

    token = ''

    class WrongStatus(Exception):
        pass

    @staticmethod
    def unpack(data):
        if data.status_code != requests.codes.ok:
            return None

        result = data.json()
        print(result)
        if result['code'] != 0:
            print("IAMPORT ERROR: " + result['message'])
            return None

        return result['response']

    def auth(self):
        res = requests.post(self.api_base + self.api_auth, json={
            'imp_key': settings.PAYMENT_REST_KEY,
            'imp_secret': settings.PAYMENT_REST_SECRET
        })
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        self.token = unpacked['access_token']
        return True

    def payment(self, imp_uid):
        if not self.token:
            raise IamportRest.WrongStatus()

        res = requests.get(self.api_base + self.api_result + imp_uid, headers={'Authorization': self.token})
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        return unpacked

    def prepare(self, uid, amount):
        if not self.token:
            raise IamportRest.WrongStatus()

        res = requests.post(self.api_base + self.api_prepare, json={
            'merchant_uid': uid,
            'amount': amount
        }, headers={'Authorization': self.token})
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        if unpacked['merchant_uid'] == uid and unpacked['amount'] == amount:
            return True

        return False

    def cancel(self, imp_uid, merchant_uid, reason):
        if not self.token:
            raise IamportRest.WrongStatus()

        res = requests.post(self.api_base + self.api_cancel, json={
            'imp_uid': imp_uid,
            'merchant_uid': merchant_uid,
            'reason': reason
        }, headers={'Authorization': self.token})
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        return True