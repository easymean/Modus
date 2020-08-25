import jwt
import datetime

from accounts.models import Users
from my_settings import SECRET_KEY, ALGORITHM

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def generate_token(user_id, nickname):
    payload = {'id': user_id,
               'nickname': nickname,
               'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    access_token = jwt.encode(
        payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    access_token = access_token.decode('utf-8')
    return access_token


def set_token(response, token_str):
    response.set_cookie('access_token', token_str)
    return response


def get_token(request):
    token_str = request.COOKIES.get('access_token')
    if not token_str:
        return None
    return token_str


def check_token(token_str):

    try:
        payload = jwt.decode(token_str, SECRET_KEY, ALGORITHM)
        exp = payload.get('exp')
        if datetime.datetime.utcnow() > exp:
            return None

        user_nickname = payload['nickname']
        user_id = payload['id']

        user = Users.objects.filter(pk=user_id, nickname=user_nickname)

    except jwt.exceptions.DecodeError:
        return None
    except ObjectDoesNotExist:
        return None

    return user
