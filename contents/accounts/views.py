import json
from .models import Users

from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status)


class UserCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data['email']
            if not email:
                raise ValueError('이메일을 입력해주세요')

            if Users.objects.filter(email=email).exists():
                raise ValueError('이미 존재하는 이메일입니다.')

            nickname = data['nickname']
            password = data['password']
            user = Users.objects.create_user(email, nickname, password)

            return self.response(user, 'success', 200)

        except ValueError:
            return self.response({}, 'fail', 400)
