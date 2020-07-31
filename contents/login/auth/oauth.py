import requests
from urllib.parse import urlencode

from django.shortcuts import redirect
from my_settings import KAKAO_KEY, NAVER_KEY, NAVER_SECRET


def oauth(request):
    code = request.GET['code']
    return code


class NaverClient:
    client_id = NAVER_KEY
    client_secret = NAVER_SECRET
    grant_type = 'authorization_code'

    auth_url = 'https://nid.naver.com/oauth2.0/token'
    profile_url = 'https://openapi.naver.com/v1/nid/me'

    base_url = 'https://nid.naver.com/oauth2.0/authorize?'
    redirect_uri = "http://127.0.0.1:8000/auth/login/naver"

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_redirect_url(self):
        state_string = self.redirect_uri.encode('utf-8')
        params = {
            'client_id': self.client_id, 'redirect_uri': self.redirect_uri,
            'response_type': 'code', 'state': state_string}
        url = self.base_url + urlencode(params)
        return url

    # oauth 서버에서 토큰을 받기 위해 요청을 보냅니다.
    def get_access_token(self, code):  # res is token request
        res = requests.get(self.auth_url, params={
            'client_id': self.client_id, 'client_secret': self.client_secret,
            'grant_type': self.grant_type, 'code': code})
        return res.json()

    # 4. oauth 서버에서 유저 정보(token and profile)를 받아옵니다.
    def get_profile(self, access_token, token_type='Bearer'):
        token_type_value = '{} {}'.format(token_type, access_token)
        res = requests.get(self.profile_url, headers={
                           'Authorization': token_type_value})

        res = res.json()
        if res.get('resultcode') != '00':
            return False, res.get('message')
        else:
            return True, res.get('response')


class KakaoClient:
    client_id = KAKAO_KEY
    grant_type = 'authorization_code'
    redirect_uri = 'http://127.0.0.1:8000/auth/login/kakao'

    auth_url = 'https://kauth.kakao.com/oauth/token'
    profile_url = 'https://kapi.kakao.com/v2/user/me'
    base_url = 'https://kauth.kakao.com/oauth/authorize?'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_redirect_url(self):
        params = {
            'client_id': self.client_id, 'redirect_uri': self.redirect_uri,
            'response_type': 'code'}
        url = self.base_url + urlencode(params)
        return url

   # oauth 서버에서 토큰을 받기 위해 권한 증서 요청을 보냅니다.
    def get_access_token(self, code):  # res is token request
        res = requests.get(self.auth_url, params={
            'grant_type': self.grant_type, 'client_id': self.client_id,
            'redirect_uri': 'http://127.0.0.1:8000/auth/login/kakao', 'code': code})
        return res.json()

    # 4. oauth 서버에서 유저 정보(token and profile)를 받아옵니다.
    def get_profile(self, access_token, token_type='Bearer'):
        token_type_value = '{} {}'.format(token_type, access_token)
        res = requests.get(self.profile_url, headers={
                           'Authorization': token_type_value})
        return res.json()
