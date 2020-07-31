import json

from .models import Users
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic import View
from utils.common_views import BaseView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email, ValidationError
from utils.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class UserView(BaseView):
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(UserView, self).dispatch(request, *args, **kwargs)

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
            user = Users.objects.create_user(
                email=email,
                password=password,
                nickname=nickname)

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
            return self.response(message='접근권한이 없습니다.', status=400)

        try:
            user = Users.objects.get(pk=id, is_active=True)
        except ObjectDoesNotExist:
            return self.response(message='%d번 유저가 존재하지 않습니다.' % id, status=400)

        return self.response({'id': user.pk, 'email': user.email}, 'success', 200)

    # nickname과 phone_number 수정가능
    def put(self, request, id):
        user = Users.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response(message='%d번 유저가 존재하지 않습니다.' % id, status=400)

        data = json.loads(request.body)
        new_user = user.update(data)

        # 수정 필요
        return self.response(new_user, 'success', 200)

    def delete(self, request, id):
        user = Users.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response(message='%d번 유저가 존재하지 않습니다.' % id, status=400)

        user.update(is_active=False)
        return self.response(message='success', status=200)


class UserListView(BaseView):
    def get(self, request):
        user_data = Users.objects.values(is_active=True)
        return self.response(data={'user': list(user_data)}, status=200)
