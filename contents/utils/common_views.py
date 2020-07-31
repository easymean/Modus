import jwt
import datetime

from django.http import JsonResponse
from django.views.generic import View
from my_settings import SECRET_KEY, ALGORITHM


class BaseView(View):
    @staticmethod
    def response(data={}, message="", status=200):
        result = {
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)

    @staticmethod
    def listResponse(num=0, data={}, message="", status=200):
        result = {
            'num': num,
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)


def give_JWT(user_id, nickname):
    payload = {'id': user_id,
               'nickname': nickname,
               'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    access_token = jwt.encode(
        payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    access_token = access_token.decode('utf-8')
    return access_token
