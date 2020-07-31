import jwt
import json
import datetime
import requests

from accounts.models import Users
from django.http import JsonResponse
from django.shortcuts import redirect
from utils.common_views import BaseView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from my_settings import KAKAO_KEY, NAVER_KEY, NAVER_SECRET
from .auth.oauth import NaverClient, KakaoClient
from .auth.token import generate_token, set_token, get_token

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

        access_token = generate_token(user_id=user.pk, nickname=user.nickname)

        response = JsonResponse({'data': {'id': user.pk,
                                          'email': user.email}}, status=200)
        response = set_token(response, access_token)
        return response


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(BaseView):
    def post(self, request):
        reset = ''
        res = JsonResponse({'message': '로그아웃되었습니다.'}, status=200)
        res.set_cookie('access_token', reset)
        return res

# front-end: 1. 클라이언트 서버가 사용자에게 인증 페이지를 제공합니다.


class SocialLoginView(BaseView):
    def get(self, request, sns_type):
        naver = NaverClient()
        kakao = KakaoClient()
        if sns_type == 'kakao':
            redirect_url = kakao.get_redirect_url()
            return redirect(redirect_url)

        if sns_type == 'naver':
            redirect_url = naver.get_redirect_url()
            return redirect(redirect_url)


class SocialLoginCallbackView(BaseView):

    def get(self, request, sns_type):
        naver = NaverClient()
        kakao = KakaoClient()

        try:
            # 2. 인증 완료후 소셜 로그인 페이지에서 권한 증서(code grant)를 받아옵니다.
            code = request.GET.get('code')

            if sns_type == 'kakao':
                token_json = kakao.get_access_token(code)
                error = token_json.get('error', None)
                if error is not None:
                    self.response(message='INVALID_CODE', status=400)

                try:
                    access_token = token_json.get('access_token')

                    # 4. oauth 서버에서 유저 정보(token and profile)를 받아옵니다.
                    sns_info_json = kakao.get_profile(
                        access_token=access_token)

                    sns_id = sns_info_json.get('id')

                    kakao_account = sns_info_json.get('kakao_account')
                    email = kakao_account.get('email')
                    kakao_profile = kakao_account.get('profile')
                    nickname = kakao_profile.get('nickname')

                except KeyError:
                    self.response(message='INVALIDd_TOKEN', status=400)

            if sns_type == 'naver':
                token_json = naver.get_access_token(code)
                error = token_json.get("error", None)
                if error is not None:
                    self.response(message='INVALID_CODE', status=400)

                try:
                    access_token = token_json.get('access_token')

                    # 4. oauth 서버에서 유저 정보(token and profile)를 받아옵니다.
                    sns_response = naver.get_profile(access_token=access_token)

                    if not sns_response[0]:
                        return self.response(message='유저 정보 받아오는데 실패했습니다.', status=400)

                    sns_id = sns_response[1].get('id')
                    email = sns_response[1].get('email')
                    nickname = sns_response[1].get('nickname')

                except KeyError:
                    self.response(message='INVALID_TOKEN', status=400)

        except KeyError:
            self.response(message='INVALID_CODE', status=400)

        # back-end: 5. 서버가 db에 고유 id를 보내서 회원을 인증합니다.
        # 5-1. 회원이라면 일반적인 로그인과정을 진행합니다.
        if Users.objects.filter(sns_type=sns_type, sns_id=sns_id).exists():
            user = Users.objects.get(sns_type=sns_type, sns_id=sns_id)
        else:  # 5-2. 회원이 아니라면 회원가입을 진행합니다.
            user = Users(
                sns_type=sns_type,
                email=email,
                nickname=nickname,
                sns_id=sns_id,
                sns_connect_date=datetime.datetime.now())
            user.save()

        access_token = generate_token(
            user_id=user.pk, nickname=user.nickname)

        response = JsonResponse({'data': {'id': user.pk,
                                          'email': user.email}}, status=200)
        response = set_token(response, access_token)
        return response
