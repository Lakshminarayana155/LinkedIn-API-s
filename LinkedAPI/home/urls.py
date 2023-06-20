from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user', views.user, name='user'),
    path('share',views.share,name='share'),
    path('txt_post',views.txt_post,name="txt_post"),
    path('article_post',views.article_post,name="article_post"),
    path('img_post',views.img_post,name="img_post"),
    path('send_invitation',views.send_invitation,name="send_invitation")
]