import jwt
import json
import datetime

from accounts.models import Users
from django.http import JsonResponse
from utils.response_views import BaseView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.my_settings import SECRET_KEY, ALGORITHM

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(BaseView):
    def post(self, request):
        data = json.loads(request.body)

        email = data['email']
        if not email:
            return self.response(message='이메일을 입력해주세요', status=400)

        input_password = data['password']
        if not input_password:
            return self.response(message='비밀번호를 입력해주세요', status=400)

        user = Users.objects.filter(email=email)
        if not user:
            return self.response(message='이메일과 비밀번호를 확인해주세요', status=400)

        user = Users.objects.get(email=email)

        try:
            result = Users.check_password(
                hashed_password=user.password, input_password=input_password)
            if not result:
                return self.response(message='이메일과 비밀번호를 확인해주세요', status=400)
            if not user.is_active:
                return self.response(message='휴면계정입니다. 관리자에게 문의해주세요', status=400)
        except KeyError:
            return self.response({}, "INVALID_KEY", 400)

        payload = {'id': user.pk,
                   'nickname': user.nickname,
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
        access_token = jwt.encode(
            payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
        access_token = access_token.decode('utf-8')

        res = JsonResponse({'success': True}, status=200)

        res.set_cookie('access_token', access_token)
        return res


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(BaseView):
    def post(self, request):
        reset = ''
        res = JsonResponse({'success': True})
        res.set_cookie('access_token', reset)
        return res


class SocialLoginView(BaseView):
