import jwt

from accounts.models import Users
from .common_views import BaseView
from my_settings import SECRET_KEY, ALGORITHM
from django.core.exceptions import ObjectDoesNotExist
from login.auth.token import get_token


def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token_str = get_token(request)

            payload = jwt.decode(token_str, SECRET_KEY, ALGORITHM)

            user_nickname = payload['nickname']
            user_id = payload['id']
            user = Users.objects.get(
                pk=user_id, nickname=user_nickname, is_active=True)

            request.user = user

        except jwt.exceptions.DecodeError:
            BaseView.response(message='INVALID_TOKEN', status=400)
        except ObjectDoesNotExist:
            BaseView.response(message='INVALID_USER', status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
