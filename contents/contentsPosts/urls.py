from django.urls import path
from .views import ContentsPostsView

urlpatterns = [
    path('', ContentsPostsView.as_view(), name='createPosts'),
    path('<int:id>', ContentsPostsView.as_view(), name='getPost'),
    path('<int:id>', ContentsPostsView.as_view(), name='updatePost'),
    path('<int:id>', ContentsPostsView.as_view(), name='deletePost'),
]
