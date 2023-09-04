from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/', views.tweet, name='tweet'),
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/mypage/<int:id>', views.my_tweet, name='my-tweet'),
]