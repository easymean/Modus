from .views import UserView, UserListView
from django.urls import path

urlpatterns = [
    path('', UserListView.as_view(), name='getUserList'),
    path('signup', UserView.as_view(), name='signup'),
    path('<int:id>', UserView.as_view(), name='getUser'),
    path('<int:id>/password', UserView.as_view(), name='changePassword'),
    path('<int:id>/info', UserView.as_view(), name='updateInfo'),
    path('<int:id>', UserView.as_view(), name='delete'),
]
