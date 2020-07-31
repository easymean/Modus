import jwt
import datetime

from my_settings import SECRET_KEY, ALGORITHM


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
    return token_str


# def login(request):
