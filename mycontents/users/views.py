import json

from config import settings
from .mail import send_email, get_uid
from .token import account_activation_token
from my_settings import EMAIL

from utils.common_views import BaseView
from utils.decorators import login_required

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email, ValidationError
# Create your views here.

User = settings.AUTH_USER_MODEL
@method_decorator(csrf_exempt, name='dispatch')
class UserView(BaseView):
    def post(self, request):
        data = json.loads(request.body)

        email = data['email']
        if not email:
            return self.response(message='이메일을 입력해주세요', status=400)

        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='올바른 이메일을 입력해주세요', status=400)

        password = data['password']
        confirmed_password = data['confirmed_password']
        if(password != confirmed_password):
            return self.response(message='비밀번호가 일치하지 않습니다.', status=400)

        nickname = data['nickname']
        if not nickname:
            return self.response(message='닉네임을 입력해주세요', status=400)

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                nickname=nickname)

            send_email(request, user.pk)
        except IntegrityError:
            email in Users.objects.values_list('email', flat=True)
            return self.response(message='이미 존재하는 이메일입니다.', status=400)

        except ValueError:
            return self.response(message='FAIL', status=400)
        except TypeError:
            return self.response(message='FAILED_HASHED', status=400)
        except KeyError:
            return self.response(message='INVALID_KEYS', status=400)

        return self.response({'id': user.pk, 'email': user.email}, 'SUCCESS', 200)

    @login_required
    def get(self, request, id):
        request_id = request.user.pk
        if request_id != id:
            return self.response(message='INVALID ACCESS', status=400)

        try:
            user = User.objects.get(pk=id, is_active=True)
        except Users.DoesNotExist:
            return self.response(message=f'{id}번 유저가 존재하지 않습니다.', status=400)

        return self.response({'id': user.pk, 'email': user.email}, 'success', 200)

    # nickname과 phone_number 수정가능
    def put(self, request, id):
        user = User.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response(message=f"{id}번 유저가 존재하지 않습니다.", status=400)

        data = json.loads(request.body)
        new_user = user.update(data)

        # 수정 필요
        return self.response(new_user, 'success', 200)

    @login_required
    def delete(self, request, id):
        user = User.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response(message=f"{id}번 유저가 존재하지 않습니다.", status=400)

        user.update(is_active=False)
        return self.response(message='success', status=200)


class UserListView(BaseView):
    def get(self, request):
        user_data = User.objects.values(is_active=True)
        return self.response(data={'user': list(user_data)}, status=200)


class Activate(BaseView):
    def get(self, request, uid64, token):
        try:
            uid = get_uid(uid64)
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return render(request, 'accounts/signup_success.html')
            return self.response(message='AUTH_FAIL', status=400)

        except User.DoesNotExist:
            return self.response(message=f'{id}번 유저가 존재하지 않습니다.', status=400)
        except ValidationError:
            return self.response(message='TYPE_ERROR', status=400)
        except KeyError:
            return self.response(message='INVALID_KEY', status=400)
