import jwt
import json
import datetime
import requests

from accounts.models import Users
from django.http import JsonResponse
from django.shortcuts import redirect
from utils.common_views import BaseView, give_JWT
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.my_settings import KAKAO_KEY

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

        access_token = give_JWT(user_id=user.pk, nickname=user.nickname)

        res = JsonResponse({'data': {'id': user.pk,
                                     'email': user.email}}, status=200)

        res.set_cookie('access_token', access_token)
        return res


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(BaseView):
    def post(self, request):
        reset = ''
        res = JsonResponse({'message': '로그아웃되었습니다.'}, status=200)
        res.set_cookie('access_token', reset)
        return res

# front-end: 1. 클라이언트 서버가 사용자에게 인증 페이지를 제공합니다.


class KakaoLoginView(BaseView):
    def get(self, request, sns_type):
        client_id = KAKAO_KEY
        redirect_uri = f"http://127.0.0.1:8000/auth/login/{sns_type}"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )


class SocialLoginCallbackView(BaseView):
    def get(self, request, sns_type):

        try:
            # 2. 인증 완료후 소셜 로그인 페이지에서 권한 증서(code grant)를 받아옵니다.
            code = request.GET.get('code')
        # if sns_type == 'naver':
        # if sns_type == 'google':

            if sns_type == 'kakao':
                client_id = KAKAO_KEY
                redirect_uri = f'http://127.0.0.1:8000/auth/login/{sns_type}'

               # 3. 토큰을 얻기 위해 outh 서버에 권한증서(code grant)를 전달합니다.
            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")

            token_json = token_request.json()
            print(token_json)
            error = token_json.get("error", None)

            if error is not None:
                self.response(message='INVALID_CODE', status=400)

            access_token = token_json.get('access_token')

            # 4. oauth 서버에서 유저 정보(token and profile)를 받아옵니다.
            sns_info_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
                                            )

            sns_info_json = sns_info_request.json()

            sns_id = sns_info_json.get('id')

            kakao_account = sns_info_json.get('kakao_account')
            email = kakao_account.get('email')

            kakao_profile = kakao_account.get('profile')
            nickname = kakao_profile.get('nickname')

        except KeyError:
            self.response(message='INVALID_TOKEN', status=400)
        # except access_token.DoesNotExist:
        #     self.response(message='INVALID_TOKEN', status=400)

        # back-end: 5. 서버가 db에 고유 id를 보내서 회원을 인증합니다.
        # 5-1. 회원이라면 일반적인 로그인과정을 진행합니다.
        if Users.objects.filter(sns_type=sns_type, sns_id=sns_id).exists():
            user = Users.objects.get(sns_type=sns_type, sns_id=sns_id)
            access_token = give_JWT(user_id=sns_id, nickname=nickname)

            res = JsonResponse({'data': {'id': user.pk,
                                         'email': user.email}}, status=200)
            res.set_cookie('access_token', access_token)
            return res
        else:  # 5-2. 회원이 아니라면 회원가입을 진행합니다.
            user = Users(
                sns_type=sns_type,
                email=email,
                nickname=nickname,
                sns_id=sns_id,
                sns_connect_date=datetime.datetime.now())
            user.save()
            access_token = give_JWT(user_id=sns_id, nickname=nickname)

            res = JsonResponse({'data': {'id': user.pk,
                                         'email': user.email}}, status=200)
            res.set_cookie('access_token', access_token)
            return res
