from pprint import pprint

import requests
from django.conf import settings

IAMPORT_API_ENDPOINT = 'https://api.iamport.kr/'

IAMPORT_API_AUTH = '/users/getToken'
IAMPORT_API_PREPARE = '/payments/prepare'
IAMPORT_API_RESULT = '/payments/'
IAMPORT_API_CANCEL = '/payments/cancel'
IAMPORT_API_CERTIFICATION = '/certifications/'


class IamportRest:
    token = ''

    class WrongStatus(Exception):
        pass

    @staticmethod
    def unpack(data):
        if data.status_code != requests.codes.ok:
            return None

        result = data.json()
        if settings.DEBUG:
            pprint(result)

        if result['code'] != 0:
            print("IAMPORT ERROR: " + result['message'])
            return None

        return result['response']

    def auth(self):
        res = requests.post(IAMPORT_API_ENDPOINT + IAMPORT_API_AUTH, json={
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

        res = requests.get(IAMPORT_API_ENDPOINT + IAMPORT_API_RESULT + imp_uid, headers={'Authorization': self.token})
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        return unpacked

    def prepare(self, uid, amount):
        if not self.token:
            raise IamportRest.WrongStatus()

        res = requests.post(IAMPORT_API_ENDPOINT + IAMPORT_API_PREPARE, json={
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

        res = requests.post(IAMPORT_API_ENDPOINT + IAMPORT_API_CANCEL, json={
            'imp_uid': imp_uid,
            'merchant_uid': merchant_uid,
            'reason': reason
        }, headers={'Authorization': self.token})
        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        return True

    def certification(self, imp_uid):
        if not self.token:
            raise IamportRest.WrongStatus()

        res = requests.get(IAMPORT_API_ENDPOINT + IAMPORT_API_CERTIFICATION + imp_uid,
                           headers={'Authorization': self.token})

        unpacked = IamportRest.unpack(res)
        if not unpacked:
            return False

        return unpacked