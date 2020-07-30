from django.urls import path, include
from .views import LoginView, LogoutView, KakaoLoginView, SocialLoginCallbackView


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login/<sns_type>', SocialLoginCallbackView.as_view(), name='socialLogin'),
    path('login/social/<sns_type>',
         KakaoLoginView.as_view(), name='kakaoLogin')
]
