import json
import jwt

from .models import Users
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class BaseView(View):
    @staticmethod
    def response(data={}, message="", status=200):
        result = {
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)

    @staticmethod
    def list_response(num=0, data={}, message="", status=200):
        result = {
            'num': num,
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(BaseView):
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(UserView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data['email']
            if not email:
                raise ValueError('이메일을 입력해주세요')

            password = data['password']
            confirmed_password = data['confirmed_password']

            if(password != confirmed_password):
                raise ValueError('비밀번호가 일치하지 않습니다.')

            if Users.objects.filter(email=email).exists():
                raise ValueError('이미 존재하는 이메일입니다.')

            nickname = data['nickname']
            user = Users.objects.create_user(
                email=email, password=password, nickname=nickname)

            return self.response({'id': user.pk, 'email': user.email}, 'success', 200)

        except ValueError:
            return self.response({}, 'fail', 400)

    def get(self, request, id):
        try:
            user = Users.objects.get(pk=id, is_active=True)
        except ObjectDoesNotExist:
            return self.response({}, "%d에 해당하는 유저가 존재하지 않습니다" % id, 400)

        return self.response({'id': user.pk, 'email': user.email}, 'success', 200)

    def put(self, request, id):
        user = Users.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response({}, '%d에 해당하는 유저가 존재하지 않습니다' % id, 400)

        data = json.loads(request.body)
        new_user = user.update(data)

        # 수정 필요
        return self.response(new_user, 'success', 200)

    def delete(self, request, id):
        user = Users.objects.filter(pk=id, is_active=True)
        if not user:
            return self.response({}, '%d에 해당하는 유저가 존재하지 않습니다' % id, 400)

        user.update(is_active=False)
        return self.response({}, 'success', 200)


class UserListView(BaseView):
    def get(self, request):
        return "hello"
