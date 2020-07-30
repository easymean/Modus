from django.urls import path, include
from .views import LoginView, LogoutView, SocialLoginView, SocialLoginCallbackView


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login/<sns_type>', SocialLoginCallbackView.as_view(),
         name='socialLoginCallback'),
    path('login/social/<sns_type>',
         SocialLoginView.as_view(), name='socialLogin')
]
