import json
import jwt

from accounts.models import Users
from .response_views import BaseView
from .my_settings import SECRET_KEY, ALGORITHM
from django.core.exceptions import ObjectDoesNotExist


def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            cookie_str = request.headers.get('Cookie')
            token_str = cookie_str.split('=')[1]
            print(token_str)

            user_info = jwt.decode(token_str, SECRET_KEY, ALGORITHM)
            user_nickname = user_info['nickname']
            user_id = user_info['id']
            user = Users.objects.get(
                pk=user_id, nickname=user_nickname, is_active=True)

            request.user = user

        except jwt.exceptions.DecodeError:
            BaseView.response(message='INVALUD_TOKEN', status=400)
        except ObjectDoesNotExist:
            BaseView.response(message='INVALID_USER', status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
