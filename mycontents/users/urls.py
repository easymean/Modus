from .views import UserView, UserListView, Activate
from django.urls import path

urlpatterns = [
    path('', UserListView.as_view(), name='getUserList'),
    path('signup', UserView.as_view(), name='signUp'),
    path('activate/<str:uid64>/<str:token>',
         Activate.as_view(), name='activate'),
    path('<int:id>', UserView.as_view(), name='getUser'),
    path('<int:id>/password', UserView.as_view(), name='changePassword'),
    path('<int:id>/info', UserView.as_view(), name='updateInfo'),
    path('<int:id>', UserView.as_view(), name='delete'),
]
